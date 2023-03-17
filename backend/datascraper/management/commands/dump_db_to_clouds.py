from django.core.management.base import BaseCommand
from datetime import datetime
import yadisk
from dotenv import load_dotenv
import os
import tg_logger
import zipfile
from datascraper.logging import init_logger
from datascraper.models import elapsed_time_decorator
import subprocess

LOGGER = init_logger('Dump database to Clouds')


class Command(BaseCommand):
    help = 'Dump data from database to Cloud services.'

    @elapsed_time_decorator(LOGGER)
    def handle(self, *args, **kwargs):

        # making dump file
        dt = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        dump_file_name = f"{dt}_dump_db"

        # for reading environmental vars
        load_dotenv()
        postgres_db = os.environ["POSTGRES_DB"]
        postgres_user = os.environ["POSTGRES_USER"]

        # reading from .env
        postgres_db = os.environ.get("POSTGRES_DB")
        postgres_user = os.environ.get("POSTGRES_USER")
        postgres_password = os.environ.get("POSTGRES_PASSWORD")
        postgres_host = os.environ.get("POSTGRES_HOST")
        postgres_port = os.environ.get("POSTGRES_PORT")

        # creating dump file
        process = subprocess.Popen(
            ['pg_dump',
                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(
                    postgres_user,
                    postgres_password,
                    postgres_host,
                    postgres_port,
                    postgres_db),
                '-Fc',
                '-f', dump_file_name,
                '-v'],
            stdout=subprocess.PIPE)

        if int(process.returncode) != 0:
            LOGGER.debug('Command failed. Return code : {}'.format(
                process.returncode))
            exit(1)

        LOGGER.debug("Dump file created")

        # zipping dump file
        with zipfile.ZipFile(f'{dump_file_name}.zip', 'w',
                             compression=zipfile.ZIP_DEFLATED) as myzip:
            myzip.write(dump_file_name)
        LOGGER.debug("Dump file archived")

        # sending dump to Yandex Disk
        try:
            yandex = yadisk.YaDisk(token=os.environ["YANDEX_TOKEN"])
            yandex.upload(f'{dump_file_name}.zip',
                          f'agweather_dump_db/{dump_file_name}.zip',
                          timeout=(100, 100))
        except Exception as e:
            LOGGER.error(e)
        LOGGER.debug("Sent to Yandex Disk")

        # sending dump to Telegram (file size limit 50M)
        try:
            token = os.environ["TELEGRAM_TOKEN"]
            users = os.environ["TELEGRAM_USERS"].split('\n')
            tg_files_logger = tg_logger.TgFileLogger(
                token=token,
                users=users,
                timeout=10
            )
            tg_files_logger.send(f'{dump_file_name}.zip')
        except Exception as e:
            LOGGER.error(e)

        # removing temp files
        os.remove(dump_file_name)
        os.remove(f'{dump_file_name}.zip')

        LOGGER.debug("Sent to Telegram")

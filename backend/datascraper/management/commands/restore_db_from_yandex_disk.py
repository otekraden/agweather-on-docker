from django.core.management.base import BaseCommand
import yadisk
from dotenv import load_dotenv
import os
from datascraper.logging import init_logger
from datascraper.models import elapsed_time_decorator
import subprocess

LOGGER = init_logger('Recover database from Yandex Disk')


class Command(BaseCommand):
    help = 'Recover database from Yandex Disk'

    @elapsed_time_decorator(LOGGER)
    def handle(self, *args, **kwargs):

        # for reading environmental vars
        load_dotenv()

        # loading dump file from Yandex Disk
        yandex = yadisk.YaDisk(token=os.environ["YANDEX_TOKEN"])
        last_dump_file = next(yandex.get_last_uploaded())
        last_dump_file_name = last_dump_file.name
        last_dump_file.download(last_dump_file_name)

        # unzipping dump file
        os.system(f"unzip {last_dump_file_name}")
        os.remove(last_dump_file_name)
        last_dump_file_name = last_dump_file_name.replace(".zip", "")

        # reading from .env
        postgres_db = os.environ.get("POSTGRES_DB")
        postgres_user = os.environ.get("POSTGRES_USER")
        postgres_password = os.environ.get("POSTGRES_PASSWORD")
        postgres_host = os.environ.get("POSTGRES_HOST")
        postgres_port = os.environ.get("POSTGRES_PORT")

        # restoring data from dump file
        process = subprocess.Popen(
            ['pg_restore',
                '--no-owner',
                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(
                    postgres_user,
                    postgres_password,
                    postgres_host,
                    postgres_port,
                    postgres_db),
                '-c',
                last_dump_file_name],
            stdout=subprocess.PIPE)

        output = process.communicate()[0]

        os.remove(last_dump_file_name)

        if int(process.returncode) != 0:
            LOGGER.debug('Command failed. Return code : {}'.format(
                process.returncode))
            return output

        else:
            LOGGER.debug("Database successfully recovered from Yandex Disk.")

from django.core.management.base import BaseCommand
from datetime import datetime
import yadisk
import os
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

        # creating dump file
        process = subprocess.run(
            ['pg_dump',
                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(
                    os.environ.get("POSTGRES_USER"),
                    os.environ.get("POSTGRES_PASSWORD"),
                    os.environ.get("POSTGRES_HOST"),
                    os.environ.get("POSTGRES_PORT"),
                    os.environ.get("POSTGRES_DB")),
                '-Fc',
                # '-v',
                '-f',
                dump_file_name])

        if process.returncode:
            LOGGER.debug('Command failed. Return code : {}'.format(
                process.returncode))
            exit(1)

        LOGGER.debug("Dump file created")

        # sending dump to Yandex Disk
        try:
            yandex = yadisk.YaDisk(token=os.environ.get("YANDEX_TOKEN"))
            yandex.upload(f'{dump_file_name}',
                          f'agweather_dump_db/{dump_file_name}',
                          timeout=(100, 100))
        except Exception as e:
            LOGGER.error(e)
        LOGGER.debug("Sent to Yandex Disk")

        # removing temp files
        os.remove(dump_file_name)

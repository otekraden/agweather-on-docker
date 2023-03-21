from django.core.management.base import BaseCommand
import yadisk
import os
from datascraper.logging import init_logger
from datascraper.models import elapsed_time_decorator
import subprocess

LOGGER = init_logger('Recover data from Yandex Disk')


class Command(BaseCommand):
    help = 'Recover database & media folder from Yandex Disk'

    @elapsed_time_decorator(LOGGER)
    def handle(self, *args, **kwargs):

        # loading dump from Yandex Disk
        yandex = yadisk.YaDisk(token=os.environ.get("YANDEX_TOKEN"))
        last_dump = next(yandex.get_last_uploaded())
        last_dump_name = last_dump.name
        LOGGER.debug(f'Last dump archive detected: {last_dump_name}')
        last_dump.download(last_dump_name)

        # unzipping dump
        LOGGER.debug('Start unzipping archive')
        subprocess.run(['unzip', '-uq', f'{last_dump_name}'])

        # restoring data from dump file
        LOGGER.debug("Start recovering database")
        db_file_name = last_dump_name.replace('_dump.zip', '_db')
        process = subprocess.run(
            ['pg_restore',
                '--no-owner',
                '--dbname=postgresql://{}:{}@{}:{}/{}'.format(
                    os.environ.get("POSTGRES_USER"),
                    os.environ.get("POSTGRES_PASSWORD"),
                    os.environ.get("POSTGRES_HOST"),
                    os.environ.get("POSTGRES_PORT"),
                    os.environ.get("POSTGRES_DB")),
                '-c',
                db_file_name])

        # os.remove(last_dump_file_name)

        if process.returncode:
            LOGGER.debug('Command failed. Return code : {}'.format(
                process.returncode))
            exit(1)

        else:
            LOGGER.debug("Database successfully recovered from Yandex Disk.")

        # removing temp files
        os.remove(db_file_name)
        os.remove(last_dump_name)

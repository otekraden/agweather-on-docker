from django.core.management.base import BaseCommand
import yadisk
import os
from datascraper.logging import init_logger
from datascraper.models import elapsed_time_decorator
import subprocess

LOGGER = init_logger('Recover database from Yandex Disk')


class Command(BaseCommand):
    help = 'Recover database from Yandex Disk'

    @elapsed_time_decorator(LOGGER)
    def handle(self, *args, **kwargs):

        # loading dump file from Yandex Disk
        yandex = yadisk.YaDisk(token=os.environ.get("YANDEX_TOKEN"))
        last_dump_file = next(yandex.get_last_uploaded())
        last_dump_file_name = last_dump_file.name
        LOGGER.debug(f'Last dump file detected: {last_dump_file_name}')
        last_dump_file.download(last_dump_file_name)

        # restoring data from dump file
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
                last_dump_file_name])

        os.remove(last_dump_file_name)

        if process.returncode:
            LOGGER.debug('Command failed. Return code : {}'.format(
                process.returncode))
            exit(1)

        else:
            LOGGER.debug("Database successfully recovered from Yandex Disk.")

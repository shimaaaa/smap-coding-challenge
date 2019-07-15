from pathlib import Path

from django.core.management.base import BaseCommand

from consumption.management.commands.logic.data_import import DataImportLogic
from consumption.management.commands.logic.reader import DataFileReader


class Command(BaseCommand):
    help = 'import data'

    @classmethod
    def _get_target_directory(cls) -> Path:
        return Path(__file__).resolve().parent.parent.parent.parent.parent / Path('data')

    def handle(self, *args, **options):
        target_dir = self._get_target_directory()

        data_reader = DataFileReader(target_dir=target_dir)

        logic = DataImportLogic(
            data_reader=data_reader
        )

        logic.execute()

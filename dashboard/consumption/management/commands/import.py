from pathlib import Path
from datetime import datetime
import argparse

from django.core.management.base import BaseCommand

from consumption.management.commands.logic.data_import import DataImportLogic
from consumption.management.commands.logic.reader import DataFileReader


class Command(BaseCommand):
    help = 'import data'

    def add_arguments(self, parser):
        parser.add_argument('--summary-from',
                            action='store',
                            dest='summary_from',
                            type=self.valid_date,
                            help='start date for creating summary (if you need only create summary data)')

    @classmethod
    def valid_date(cls, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(value)
            raise argparse.ArgumentTypeError(msg)

    @classmethod
    def _get_target_directory(cls) -> Path:
        return Path(__file__).resolve().parent.parent.parent.parent.parent / Path('data')

    def handle(self, *args, **options):
        target_dir = self._get_target_directory()

        data_reader = DataFileReader(target_dir=target_dir)

        logic = DataImportLogic(
            data_reader=data_reader
        )

        summary_from = options.get('summary_from')
        if summary_from is not None:
            logic.create_summary(summary_from)
            return
        logic.import_data()

from logging import getLogger
from typing import Optional
from datetime import datetime

from consumption.management.commands.logic.reader import DataReader
from consumption.management.commands.logic.importer import DataImporter, DatabaseImporter

logger = getLogger(__name__)


class DataImportLogic:
    USER_BULK_IMPORT_COUNT = 50
    CONSUMPTION_BULK_IMPORT_COUNT = 500

    def __init__(self,
                 data_reader: DataReader,
                 data_importer: Optional[DataImporter] = None):
        self._data_reader = data_reader
        self._data_importer = data_importer or DatabaseImporter()

    def _import_user_data(self):
        count = 0
        users = list()

        for user in self._data_reader.read_user():
            count += 1
            users.append(user)
            if count % self.USER_BULK_IMPORT_COUNT == 0:
                self._data_importer.user_bulk_import(users)
                users.clear()

        if users:
            self._data_importer.user_bulk_import(users)

    def _import_consumption_data(self):
        count = 0
        consumptions = list()
        consumption_datetime_from = None

        for consumption in self._data_reader.read_consumption():
            count += 1
            consumptions.append(consumption)

            if consumption_datetime_from is None or consumption_datetime_from > consumption.target_datetime:
                consumption_datetime_from = consumption.target_datetime

            if count % self.CONSUMPTION_BULK_IMPORT_COUNT == 0:
                self._data_importer.consumption_bulk_import(consumptions)
                consumptions.clear()

        if consumptions:
            self._data_importer.consumption_bulk_import(consumptions)
        return consumption_datetime_from

    def _import_summary_data(self, consumption_datetime_from):
        self._data_importer.summary_import(consumption_datetime_from)

    def import_data(self):
        logger.info('import user data')
        self._import_user_data()
        logger.info('import consumption data')
        consumption_datetime_from = self._import_consumption_data()
        self.create_summary(consumption_datetime_from)

    def create_summary(self, consumption_datetime_from: datetime):
        self._import_summary_data(consumption_datetime_from)

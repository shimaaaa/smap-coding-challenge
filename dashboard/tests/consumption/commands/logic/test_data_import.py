from typing import List
from datetime import datetime

import pytz

from django.test import TestCase

from consumption.management.commands.logic.dto import UserData as UserDataDto
from consumption.management.commands.logic.dto import ConsumptionData as ConsumptionDataDto
from consumption.management.commands.logic.reader import DataReader
from consumption.management.commands.logic.importer import DataImporter
from consumption.management.commands.logic.data_import import DataImportLogic


class DummyDataReader(DataReader):
    def __init__(self,
                 users: List[UserDataDto],
                 consumptions: List[ConsumptionDataDto]):
        self.users = users
        self.consumptions = consumptions

    def read_user(self):
        for user in self.users:
            yield user

    def read_consumption(self):
        for consumption in self.consumptions:
            yield consumption


class DummyDataImporter(DataImporter):
    def __init__(self):
        self.user_import_counter = 0
        self.consumption_import_counter = 0

    def user_bulk_import(self, users: List[UserDataDto]):
        self.user_import_counter += 1

    def consumption_bulk_import(self, consumptions: List[ConsumptionDataDto]):
        self.consumption_import_counter += 1

    def summary_import(self, target_datetime_from=None):
        pass


class DataImportLogicTest(TestCase):
    TEST_USER_DATA = [
        UserDataDto(3000, 'a1', 't1'),
        UserDataDto(3001, 'a2', 't2')
    ]
    TEST_CONSUMPTION_DATA = [
        ConsumptionDataDto(3000, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC), 12.2),
        ConsumptionDataDto(3000, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), 13.2),
        ConsumptionDataDto(3001, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC), 14.2),
    ]

    def test_execute(self):
        reader = DummyDataReader(users=self.TEST_USER_DATA, consumptions=self.TEST_CONSUMPTION_DATA)
        importer = DummyDataImporter()
        logic = DataImportLogic(
            data_reader=reader,
            data_importer=importer
        )
        logic.import_data()

        self.assertEqual(importer.user_import_counter, 1)
        self.assertEqual(importer.consumption_import_counter, 1)

    def test_execute_update_bulk_count(self):
        reader = DummyDataReader(users=self.TEST_USER_DATA, consumptions=self.TEST_CONSUMPTION_DATA)
        importer = DummyDataImporter()
        logic = DataImportLogic(
            data_reader=reader,
            data_importer=importer
        )
        logic.USER_BULK_IMPORT_COUNT = 1
        logic.CONSUMPTION_BULK_IMPORT_COUNT = 2
        logic.import_data()

        self.assertEqual(importer.user_import_counter, 2)
        self.assertEqual(importer.consumption_import_counter, 2)

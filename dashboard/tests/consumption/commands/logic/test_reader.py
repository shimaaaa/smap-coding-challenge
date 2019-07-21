from pathlib import Path
from datetime import datetime

import pytz
from django.test import TestCase

from consumption.management.commands.logic.reader import DataFileReader


class DataFileReaderTest(TestCase):
    TARGET_DATA_DIRECTORY = None
    TARGET_BROKEN_DATA_DIRECTORY = None

    @classmethod
    def _get_target_directory(cls) -> Path:
        return Path(__file__).resolve().parent.parent.parent.parent / Path('data')

    @classmethod
    def _get_broken_target_directory(cls) -> Path:
        return Path(__file__).resolve().parent.parent.parent.parent / Path('data-broken')

    @classmethod
    def setUpClass(cls):
        cls.TARGET_DATA_DIRECTORY = cls._get_target_directory()
        cls.TARGET_BROKEN_DATA_DIRECTORY = cls._get_broken_target_directory()
        super().setUpClass()

    def test_read_user(self):
        reader = DataFileReader(self.TARGET_DATA_DIRECTORY)
        user_generator = reader.read_user()

        user = user_generator.__next__()
        self.assertEqual(user.user_id, 3000)
        self.assertEqual(user.area, 'a1')
        self.assertEqual(user.tariff, 't2')

        user = user_generator.__next__()
        self.assertEqual(user.user_id, 3001)
        self.assertEqual(user.area, 'a2')
        self.assertEqual(user.tariff, 't1')

        with self.assertRaises(StopIteration):
            user_generator.__next__()

    def test_read_broken_user_data(self):
        reader = DataFileReader(self.TARGET_BROKEN_DATA_DIRECTORY)
        user_generator = reader.read_user()

        user = user_generator.__next__()
        self.assertEqual(user.user_id, 3000)
        self.assertEqual(user.area, 'a1')
        self.assertEqual(user.tariff, 't2')

        with self.assertRaises(StopIteration):
            user_generator.__next__()

    def test_read_consumption_data(self):
        reader = DataFileReader(self.TARGET_DATA_DIRECTORY)
        consumption_generator = reader.read_consumption()

        consumption = consumption_generator.__next__()
        self.assertEqual(consumption.user_id, 3000)
        self.assertEqual(consumption.value, 39.0)
        self.assertEqual(consumption.target_datetime, datetime(2016, 7, 15, 0, 0, 0, tzinfo=pytz.UTC))

        consumption = consumption_generator.__next__()
        self.assertEqual(consumption.user_id, 3000)
        self.assertEqual(consumption.value, 147.0)
        self.assertEqual(consumption.target_datetime, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC))

        consumption = consumption_generator.__next__()
        self.assertEqual(consumption.user_id, 3001)
        self.assertEqual(consumption.value, 378.0)
        self.assertEqual(consumption.target_datetime, datetime(2016, 7, 15, 0, 0, 0, tzinfo=pytz.UTC))

        consumption = consumption_generator.__next__()
        self.assertEqual(consumption.user_id, 3001)
        self.assertEqual(consumption.value, 341.0)
        self.assertEqual(consumption.target_datetime, datetime(2016, 7, 15, 0, 30, 1, tzinfo=pytz.UTC))

        with self.assertRaises(StopIteration):
            consumption_generator.__next__()

    def test_read_consumption_broken_data(self):
        reader = DataFileReader(self.TARGET_BROKEN_DATA_DIRECTORY)
        consumption_generator = reader.read_consumption()

        consumption = consumption_generator.__next__()
        self.assertEqual(consumption.user_id, 3000)
        self.assertEqual(consumption.value, 39.0)
        self.assertEqual(consumption.target_datetime, datetime(2016, 7, 15, 0, 0, 0, tzinfo=pytz.UTC))

        consumption = consumption_generator.__next__()
        self.assertEqual(consumption.user_id, 3000)
        self.assertEqual(consumption.value, 147.0)
        self.assertEqual(consumption.target_datetime, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC))

        consumption = consumption_generator.__next__()
        self.assertEqual(consumption.user_id, 3001)
        self.assertEqual(consumption.value, 378.0)
        self.assertEqual(consumption.target_datetime, datetime(2016, 7, 15, 0, 0, 0, tzinfo=pytz.UTC))

        with self.assertRaises(StopIteration):
            consumption_generator.__next__()

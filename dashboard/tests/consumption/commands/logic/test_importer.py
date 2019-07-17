from collections import defaultdict
from statistics import mean
from datetime import datetime, date
from decimal import Decimal

import pytz
from django.test import TestCase

from consumption.models import Users, UserConsumptions, ConsumptionDailySummary
from consumption.management.commands.logic.dto import UserData, ConsumptionData
from consumption.management.commands.logic.importer import DatabaseImporter


class DatabaseImporterTest(TestCase):

    TEST_USER_DATA = [
        UserData(3000, 'a1', 't1'),
        UserData(3001, 'a2', 't2')
    ]
    TEST_USER_DUPLICATE_DATA = [
        UserData(3000, 'a1', 't1'),
        UserData(3001, 'a2', 't2'),
        UserData(3001, 'a1', 't1')
    ]
    TEST_CONSUMPTION_DATA = [
        ConsumptionData(3000, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC), 12.2),
        ConsumptionData(3000, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), 13.2),
        ConsumptionData(3001, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC), 14.2),
    ]
    TEST_CONSUMPTION_DUPLICATE_DATA = [
        ConsumptionData(3000, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC), 12.2),
        ConsumptionData(3000, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), 13.2),
        ConsumptionData(3001, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC), 14.2),
        ConsumptionData(3000, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC), 19.2),
    ]
    TEST_CONSUMPTION_INVALID_USER_DATA = [
        ConsumptionData(3000, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC), 12.2),
        ConsumptionData(3000, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), 13.2),
        ConsumptionData(3001, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC), 14.2),
        ConsumptionData(1, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC), 14.2),
    ]
    TEST_CONSUMPTION_DATA_FOR_SUMMARY = [
        ConsumptionData(3000, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC), 12.2),
        ConsumptionData(3000, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), 13.2),
        ConsumptionData(3001, datetime(2016, 7, 14, 1, 0, 0, tzinfo=pytz.UTC), 14.2),
    ]

    def test_user_bulk_import(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DATA)

        users = Users.objects.all()

        self.assertEqual(len(users), 2)

        user = users[0]
        self.assertEqual(user.id, 3000)
        self.assertEqual(user.area, 'a1')
        self.assertEqual(user.tariff, 't1')

        user = users[1]
        self.assertEqual(user.id, 3001)
        self.assertEqual(user.area, 'a2')
        self.assertEqual(user.tariff, 't2')

    def test_duplicate_user_bulk_import(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DUPLICATE_DATA)

        users = Users.objects.all()

        self.assertEqual(len(users), 2)

        user = users[0]
        self.assertEqual(user.id, 3000)
        self.assertEqual(user.area, 'a1')
        self.assertEqual(user.tariff, 't1')

        user = users[1]
        self.assertEqual(user.id, 3001)
        self.assertEqual(user.area, 'a2')
        self.assertEqual(user.tariff, 't2')

    def test_consumption_bulk_import(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DATA)

        importer.consumption_bulk_import(self.TEST_CONSUMPTION_DATA)

        consumptions = UserConsumptions.objects.all()

        self.assertEqual(len(consumptions), 3)

        consumption = consumptions[0]
        self.assertEqual(consumption.user.id, 3000)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('12.2'))

        consumption = consumptions[1]
        self.assertEqual(consumption.user.id, 3000)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('13.2'))

        consumption = consumptions[2]
        self.assertEqual(consumption.user.id, 3001)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('14.2'))

    def test_duplicate_consumption_bulk_import(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DATA)

        importer.consumption_bulk_import(self.TEST_CONSUMPTION_DUPLICATE_DATA)

        consumptions = UserConsumptions.objects.all()

        self.assertEqual(len(consumptions), 3)

        consumption = consumptions[0]
        self.assertEqual(consumption.user.id, 3000)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('12.2'))

        consumption = consumptions[1]
        self.assertEqual(consumption.user.id, 3000)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('13.2'))

        consumption = consumptions[2]
        self.assertEqual(consumption.user.id, 3001)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('14.2'))

    def test_invalid_user_consumption_bulk_import(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DATA)

        importer.consumption_bulk_import(self.TEST_CONSUMPTION_INVALID_USER_DATA)

        consumptions = UserConsumptions.objects.all()

        self.assertEqual(len(consumptions), 3)

        consumption = consumptions[0]
        self.assertEqual(consumption.user.id, 3000)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('12.2'))

        consumption = consumptions[1]
        self.assertEqual(consumption.user.id, 3000)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('13.2'))

        consumption = consumptions[2]
        self.assertEqual(consumption.user.id, 3001)
        self.assertEqual(consumption.datetime, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC))
        self.assertEqual(consumption.consumption, Decimal('14.2'))

    def test_summary_import(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DATA)
        importer.consumption_bulk_import(self.TEST_CONSUMPTION_DATA_FOR_SUMMARY)

        importer.summary_import()

        consumptions = UserConsumptions.objects.all()
        consumption_per_date = defaultdict(list)
        for consumptions in consumptions:
            consumption_per_date[consumptions.datetime.strftime('%Y-%m-%d')].append(consumptions.consumption)

        summary_list = ConsumptionDailySummary.objects.all()

        self.assertEqual(len(summary_list), 2)

        summary = summary_list[0]
        consumption_summary_data = consumption_per_date['2016-07-14']
        self.assertEqual(summary.target_date, date(2016, 7, 14))
        self.assertEqual(summary.total_consumption, sum(consumption_summary_data))
        self.assertEqual(summary.average_consumption, mean(consumption_summary_data))

        summary = summary_list[1]
        consumption_summary_data = consumption_per_date['2016-07-15']
        self.assertEqual(summary.target_date, date(2016, 7, 15))
        self.assertEqual(summary.total_consumption, sum(consumption_summary_data))
        self.assertEqual(summary.average_consumption, mean(consumption_summary_data))

    def test_summary_import_specific_datetime(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DATA)
        importer.consumption_bulk_import(self.TEST_CONSUMPTION_DATA_FOR_SUMMARY)

        importer.summary_import(datetime(2016, 7, 15, 0, 0, 0, tzinfo=pytz.UTC))

        consumptions = UserConsumptions.objects.all()
        consumption_per_date = defaultdict(list)
        for consumptions in consumptions:
            consumption_per_date[consumptions.datetime.strftime('%Y-%m-%d')].append(consumptions.consumption)

        summary_list = ConsumptionDailySummary.objects.all()

        self.assertEqual(len(summary_list), 1)

        summary = summary_list[0]
        consumption_summary_data = consumption_per_date['2016-07-15']
        self.assertEqual(summary.target_date, date(2016, 7, 15))
        self.assertEqual(summary.total_consumption, sum(consumption_summary_data))
        self.assertEqual(summary.average_consumption, mean(consumption_summary_data))

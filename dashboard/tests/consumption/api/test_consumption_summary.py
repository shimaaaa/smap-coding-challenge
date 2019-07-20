from datetime import datetime
from collections import defaultdict
from statistics import mean

import pytz
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from consumption.models import UserConsumption
from consumption.management.commands.logic.dto import UserData, ConsumptionData
from consumption.management.commands.logic.importer import DatabaseImporter


class APIUserTest(APITestCase):
    TEST_USER_DATA = [
        UserData(3000, 'a1', 't1'),
        UserData(3001, 'a2', 't2')
    ]
    TEST_CONSUMPTION_DATA = [
        ConsumptionData(3000, datetime(2016, 7, 14, 0, 0, 0, tzinfo=pytz.UTC), 12.2),
        ConsumptionData(3000, datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), 13.2),
        ConsumptionData(3001, datetime(2016, 7, 15, 1, 0, 0, tzinfo=pytz.UTC), 14.2),
    ]

    def setUp(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DATA)
        importer.consumption_bulk_import(self.TEST_CONSUMPTION_DATA)
        importer.summary_import()

    def test_user_list(self):
        url = reverse('summary-list')
        data = dict()
        response = self.client.get(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        summary_list = response.data

        self.assertEqual(len(summary_list), 2)

        consumptions = UserConsumption.objects.all()
        consumption_per_date = defaultdict(list)
        for consumption in consumptions:
            consumption_per_date[consumption.target_datetime.strftime('%Y-%m-%d')].append(consumption.value)

        summary = summary_list[0]
        consumption_summary_data = consumption_per_date['2016-07-14']
        self.assertEqual(summary['target_date'], '2016-07-14')
        self.assertEqual(summary['total_value'], str(sum(consumption_summary_data)))
        self.assertEqual(summary['average_value'], str(mean(consumption_summary_data)))

        summary = summary_list[1]
        consumption_summary_data = consumption_per_date['2016-07-15']
        self.assertEqual(summary['target_date'], '2016-07-15')
        self.assertEqual(summary['total_value'], str(sum(consumption_summary_data)))
        self.assertEqual(summary['average_value'], str(mean(consumption_summary_data)))

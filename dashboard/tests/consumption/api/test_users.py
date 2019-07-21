from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from consumption.management.commands.logic.dto import UserData
from consumption.management.commands.logic.importer import DatabaseImporter


class APIUserTest(APITestCase):
    TEST_USER_DATA = [
        UserData(3000, 'a1', 't1'),
        UserData(3001, 'a2', 't2')
    ]

    def setUp(self):
        importer = DatabaseImporter()
        importer.user_bulk_import(self.TEST_USER_DATA)

    def test_user_list(self):
        url = reverse('users-list')
        data = dict()
        response = self.client.get(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        users = response.data
        self.assertEqual(len(users), 2)

        user = users[0]
        self.assertEqual(user['id'], 3000)
        self.assertEqual(user['area'], 'a1')
        self.assertEqual(user['tariff'], 't1')

        user = users[1]
        self.assertEqual(user['id'], 3001)
        self.assertEqual(user['area'], 'a2')
        self.assertEqual(user['tariff'], 't2')

    def test_user_list_with_search(self):
        url = reverse('users-list')
        data = dict(search='3000')
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        users = response.data
        self.assertEqual(len(users), 1)

        user = users[0]
        self.assertEqual(user['id'], 3000)
        self.assertEqual(user['area'], 'a1')
        self.assertEqual(user['tariff'], 't1')

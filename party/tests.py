from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import Party


class PartyAPI(APITestCase):

    def setUp(self):
        p = Party(name='Party', website='www.website.com')
        p.save()

    def test_get_all(self):
        response = self.client.get('/parties/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Party')
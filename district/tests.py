from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import District

class DistrictAPI(APITestCase):

    def setUp(self):
        district = District(name = 'Reykjavik South', abbreviation='RVK S')
        district.save()

    def test_get_all(self):
        response = self.client.get('/districts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Reykjavik South')


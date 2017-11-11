from rest_framework.test import APITestCase
from .models import Party

class PartyAPI(APITestCase):

    def setUp(self):
        p = Party(name='Píratar', website='www.pirateparty.is')
        p.save()

    def test_get_all(self):
        response = self.client.get('/api/v1/parties/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Píratar')

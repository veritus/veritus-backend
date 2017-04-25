from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import ParliamentMember
from party.models import Party
from district.models import District

class ParliamentMemberAPI(APITestCase):

    def setUp(self):
        p = Party(name='Party', website='www.website.com')
        p.save()
        d = District(name='District', abbreviation='d')
        d.save()
        pm = ParliamentMember(
            name = 'John Johnson', 
            initials = 'jj', 
            districtNumber = 10, 
            party = p,
            district = d)
        pm.save()

    def test_get_all(self):
        response = self.client.get('/api/v1/parliamentMembers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Johnson')


from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from case_gather.models import Subject

class PartyAPI(APITestCase):

    def setUp(self):
        hagstjorn = Subject(name='Hagstjórn')
        hagstjorn.save()
        fjarreidur = Subject(name='Fjárreiður ríkisins', parent=hagstjorn)
        fjarreidur.save()

    def test_get_all(self):
        response = self.client.get('/api/v1/subjects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Hagstjórn')
        self.assertEqual(response.data[1]['name'], 'Fjárreiður ríkisins')

    def test_name_full_search(self):
        response = self.client.get('/api/v1/subjects/?name=Hagstjórn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Hagstjórn')

   # def test_name_startswith_search(self):
    #    response = self.client.get('/api/v1/subjects/?name__startswith=Hag')
     #   self.assertEqual(response.status_code, 200)
      #  self.assertEqual(len(response.data), 1)
       # self.assertEqual(response.data[0]['name'], 'Hagstjórn')

    def test_name_full_search(self):
        hagstjorn = Subject.objects.filter(name='Hagstjórn').get()
        response = self.client.get('/api/v1/subjects/?parent='+str(hagstjorn.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Fjárreiður ríkisins')


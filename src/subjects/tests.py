from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from case_gather.models import Subject
from django.contrib.auth.models import User
from subjects.models import PromiseSubject
from promises.models import Promise
from parliament.models import Parliament


class PartyAPI(APITestCase):

    def setUp(self):
        lauren = User(username='lauren')
        lauren.save()
        lauren_token = Token(user=lauren)
        lauren_token.save()

        hagstjorn = Subject(name='Hagstjórn', number=1)
        hagstjorn.save()
        fjarreidur = Subject(name='Fjárreiður ríkisins',
                             parent=hagstjorn, number=2)
        fjarreidur.save()

        parliament = Parliament(
            name='Parliament', start_date='2017-01-01', end_date='2017-01-01')
        parliament.save()
        promise1 = Promise(name='Promise 1', parliament=parliament)
        promise2 = Promise(name='Promise 2', parliament=parliament)
        promise1.save()
        promise2.save()
        promise1_hagstjorn = PromiseSubject(
            subject=hagstjorn, promise=promise1)
        promise2_fjarreidur = PromiseSubject(
            subject=fjarreidur, promise=promise2)
        promise1_hagstjorn.save()
        promise2_fjarreidur.save()

    def test_get_all_subjects(self):
        response = self.client.get('/api/v1/subjects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Hagstjórn')
        self.assertEqual(response.data['results']
                         [1]['name'], 'Fjárreiður ríkisins')

    def test_name_full_search(self):
        response = self.client.get('/api/v1/subjects/?name=Hagstjórn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Hagstjórn')

    def test_name_startswith_search(self):
        response = self.client.get('/api/v1/subjects/?name__startswith=Hag')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Hagstjórn')

    def test_name_contains_search(self):
        response = self.client.get('/api/v1/subjects/?name__contains=agstj')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Hagstjórn')

    def test_name_parent_search(self):
        hagstjorn = Subject.objects.filter(name='Hagstjórn').get()
        response = self.client.get(
            '/api/v1/subjects/?parent='+str(hagstjorn.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results']
                         [0]['name'], 'Fjárreiður ríkisins')

    def test_number_search(self):
        response = self.client.get('/api/v1/subjects/?number=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Hagstjórn')

    def test_post_subject(self):
        token = Token.objects.get(user__username='lauren')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        payload = {
            "name": 'New subject'
        }
        response = self.client.post('/api/v1/subjects/', data=payload)
        self.assertEqual(response.status_code, 201)

    def test_post_subject_no_name(self):
        token = Token.objects.get(user__username='lauren')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        payload = {}
        response = self.client.post('/api/v1/subjects/', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"name": ["This field is required."]})

    def test_post_subject_no_auth(self):
        payload = {}
        response = self.client.post('/api/v1/subjects/', data=payload)
        self.assertEqual(response.status_code, 401)

    def test_get_all_promise_subjects(self):
        response = self.client.get('/api/v1/promises/subjects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_get_all_promise_subjects_filter_by_promise(self):
        promise = Promise.objects.filter(name='Promise 1').get()
        response = self.client.get(
            '/api/v1/promises/subjects/?promise='+str(promise.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_get_all_promise_subjects_filter_by_subject(self):
        subject = Subject.objects.filter(name='Hagstjórn').get()
        response = self.client.get(
            '/api/v1/promises/subjects/?subject='+str(subject.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_post_promise_subject(self):
        promise = Promise.objects.filter(name='Promise 2').get()
        subject = Subject.objects.filter(name='Hagstjórn').get()
        token = Token.objects.get(user__username='lauren')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        payload = {
            "subject": subject.pk,
            "promise": promise.pk
        }
        response = self.client.post('/api/v1/promises/subjects/', data=payload)
        self.assertEqual(response.status_code, 201)

    def test_post_promise_subject_unique(self):
        promise = Promise.objects.filter(name='Promise 1').get()
        subject = Subject.objects.filter(name='Hagstjórn').get()
        token = Token.objects.get(user__username='lauren')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        payload = {
            "subject": subject.pk,
            "promise": promise.pk
        }
        response = self.client.post('/api/v1/promises/subjects/', data=payload)
        self.assertEqual(response.status_code, 400)
        expected = {'non_field_errors': [
            "The fields promise, subject must make a unique set."]}
        self.assertEqual(response.data, expected)

    def test_post_subject_and_promise_empty(self):
        token = Token.objects.get(user__username='lauren')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        payload = {}
        response = self.client.post('/api/v1/promises/subjects/', data=payload)
        self.assertEqual(response.status_code, 400)
        expected = {'subject': ['This field is required.'],
                    'promise': ['This field is required.']}
        self.assertEqual(response.data, expected)

    def test_post_subject_empty(self):
        token = Token.objects.get(user__username='lauren')
        subject = Subject.objects.filter(name='Hagstjórn').get()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        payload = {
            "subject": subject.pk
        }
        response = self.client.post('/api/v1/promises/subjects/', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            'promise': [
                'This field is required.'
            ]
        })

    def test_post_promise_empty(self):
        promise = Promise.objects.filter(name='Promise 1').get()
        token = Token.objects.get(user__username='lauren')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        payload = {
            "promise": promise.pk
        }
        response = self.client.post('/api/v1/promises/subjects/', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            'subject': [
                'This field is required.'
            ]
        })

    def test_post_subject_no_authentication(self):
        payload = {}
        response = self.client.post('/api/v1/promises/subjects/', data=payload)
        self.assertEqual(response.status_code, 401)

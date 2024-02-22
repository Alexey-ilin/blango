from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from logging import getLogger


logger = getLogger(__name__)

class UsersApiTestCase(TestCase):
    
    def setUp(self):
        self.u1 = get_user_model().objects.create(email='test@example.com', password='password')
        self.u2 = get_user_model().objects.create(email='test2@example.com', password='password')
        self.client = APIClient()
    
    def test_users_list(self):
        resp = self.client.get('/api/v1/users/')
        user_data = resp.json()['results']
        self.assertEqual(len(user_data), 2)

    def test_users_detail(self):
        resp = self.client.get(f'/api/v1/users/{self.u1.email}/')
        user_data = resp.json()
        self.assertEqual(user_data['email'], self.u1.email)
    


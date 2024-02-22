from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from rest_framework.authtoken.models import Token

from blog.models import Tag

from logging import getLogger

from datetime import datetime
from pytz import UTC

import base64

logger = getLogger(__name__)

class PostApiTestCase(TestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create(email="test@example.com", password="password")
        self.tag_data = {"tag1", "tag2", "tag3", "tag4"}
        for t in self.tag_data:
            Tag.objects.create(value=t)
        self.client = APIClient()
    
    def test_tag_list(self):
        resp = self.client.get("/api/v1/tags/")
        tags = resp.json()['results']
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Tag.objects.all().count(), len(tags))
        self.assertEqual({t['value'] for t in tags}, self.tag_data)
    
    def test_tag_create_token_auth(self):
        token = Token.objects.create(user=self.u1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        tag = {"value": "tag5"}
        resp = self.client.post("/api/v1/tags/", tag)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.all().count(), len(self.tag_data)+1)
        self.assertEqual(resp.json()["value"], tag['value'])

    def test_tag_create_basic_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Basic " + base64.b64encode("test@example.com:password".encode('utf-8')).decode())
        tag = {"value": "tag5"}
        resp = self.client.post("/api/v1/tags/", tag)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.all().count(), len(self.tag_data)+1)
        self.assertEqual(resp.json()["value"], tag['value'])

    def test_tag_create_noauth(self):
        self.client.credentials()
        tag = {"value": "tag5"}
        resp = self.client.post("/api/v1/tags/", tag)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        
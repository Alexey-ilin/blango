from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from rest_framework.authtoken.models import Token

from blog.models import Post

from logging import getLogger

from datetime import datetime
from pytz import UTC

logger = getLogger(__name__)

class PostApiTestCase(TestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create(email="test@example.com", password="passwords")
        self.u2 = get_user_model().objects.create(email="test2@example.com", password='password2')
        posts = [Post.objects.create(
                author = self.u1, 
                published_at = timezone.now(),
                title = "Test Post 1",
                slug = "test-post-1",
                summary = "Post 1",
                content = "Post 1 content",
                ),
                Post.objects.create(
                author = self.u2,
                published_at = timezone.now(),
                title = "Test Post 2",
                slug = "test-post-2",
                summary = "Post 2",
                content = "Post 2 content",
                )
                ]
        
        self.post_lookup = {p.id: p for p in posts}
        self.client = APIClient()
        token = Token.objects.create(user=self.u1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    
    def test_post_list(self):
        """test get all posts api endpoint"""
        resp = self.client.get('/api/v1/posts/')
        data = resp.json()['results']
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for post_dict in data:
            post_obj = self.post_lookup[post_dict['id']]
            self.assertTrue(post_dict['author'].endswith(f"/api/v1/users/{post_obj.author.email}/"))
            self.assertEqual(datetime.strptime(
                    post_dict["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=UTC), post_obj.published_at)
            self.assertEqual(post_dict['title'], post_obj.title)
            self.assertEqual(post_dict['slug'], post_obj.slug)
            self.assertEqual(post_dict['summary'], post_obj.summary)
            self.assertEqual(post_dict['content'], post_obj.content)
    
    
    
    #test postcreate
    def test_post_create(self):
        post_dict = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Summary",
            "content": "Test Content",
            "author": "http://testserver/api/v1/users/test@example.com",
            "published_at": "2021-01-10T09:00:00Z",
        }
        resp = self.client.post("/api/v1/posts/", post_dict)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        post_id = resp.json()["id"]
        post = Post.objects.get(pk=post_id)
        self.assertEqual(Post.objects.all().count(), 3)
        self.assertEqual(post.title, post_dict["title"])
        self.assertEqual(post.slug, post_dict["slug"])
        self.assertEqual(post.summary, post_dict["summary"])
        self.assertEqual(post.content, post_dict["content"])
        self.assertEqual(post.author, self.u1)
        self.assertEqual(post.published_at, datetime(2021, 1, 10, 9, 0, 0, tzinfo=UTC))
    
    #test postcreate
    def test_post_create_noauth(self):
        self.client.credentials()
        post_dict = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Summary",
            "content": "Test Content",
            "author": "http://testserver/api/v1/users/test@example.com",
            "published_at": "2021-01-10T09:00:00Z",
        }
        resp = self.client.post("/api/v1/posts/", post_dict)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.all().count(), 2)
    



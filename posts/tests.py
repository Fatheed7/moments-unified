from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test')

    def test_can_list_posts(self):
        test = User.objects.get(username='test')
        Post.objects.create(owner=test, title='test', content='test')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/posts/', {'title': 'test', 'content': 'test'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post_without_login(self):
        response = self.client.post('/posts/', {'title': 'test', 'content': 'test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PostDetailViewTests(APITestCase):
    def setUp(self):
        TestUser = User.objects.create_user(username='test', password='test')
        AnotherTestUser = User.objects.create_user(username='anothertest', password='anothertest')
        Post.objects.create(owner=TestUser, title='test', content='test')
        Post.objects.create(owner=AnotherTestUser, title='anothertest', content='anothertest')

    def test_can_retreieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_cannot_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='test', password='test')
        response = self.client.put('/posts/1/', {'title': 'yet another test'})
        post = Post.objects.filter(id=1).first()
        self.assertEqual(post.title, 'yet another test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_another_user_post(self):
        self.client.login(username='test', password='test')
        response = self.client.put('/posts/2/', {'title': 'yet another test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
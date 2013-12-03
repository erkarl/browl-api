from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status


class UserTest(APITestCase):

    def setUp(self):
            self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'snow')
            self.user = User.objects.create_user('tyrion', 'tyrion@lannister.com', 'lannister')
            self.factory = APIRequestFactory()

    def test_get_post_list_logged_out(self):
        """
        Ensure that everyone can GET posts-list
        """
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_list_regular_user(self):
        """
        Ensure that regular users can GET posts-list
        """
        url = reverse('post-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_list_admin(self):
        """
        Ensure that superusers can GET posts-list
        """
        url = reverse('post-list')
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_creation_admin(self):
        """
        Ensure that admin users can create new posts (POST)
        """
        url = reverse('post-list')
        user_url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        title = 'Test Title'
        body = 'Test Body'
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url, {'title': title, 'body': body, 'user': user_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(title, response.content)
        self.assertIn(body, response.content)
        self.assertIn(user_url, response.content)

    def test_post_creation_regular_user(self):
        """
        Ensure that regular users cannot create new posts
        """
        url = reverse('post-list')
        user_url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        title = 'Test Title'
        body = 'Test Body'
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {'title': title, 'body': body, 'user': user_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_creation_unauthorized(self):
        """
        Ensure that logged out users cannot create new posts
        """
        url = reverse('post-list')
        user_url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        title = 'Test Title'
        body = 'Test Body'
        response = self.client.post(url, {'title': title, 'body': body, 'user': user_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

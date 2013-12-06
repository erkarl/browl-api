from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status


class UserTest(APITestCase):

    def setUp(self):
            self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'snow')
            self.user = User.objects.create_user('tyrion', 'tyrion@lannister.com', 'lannister')
            self.factory = APIRequestFactory()

    def test_get_user_list_unauthorized(self):
        """
        Ensure that unauthorized users won't be able to GET user list
        """
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_as_regular_user(self):
        """
        Ensure that regular users won't have access to GET user list
        """
        url = reverse('user-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_as_admin(self):
        """
        Ensure that admin users have access to GET user list
        """
        url = reverse('user-list')
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.superuser.username, response.content)
        self.assertIn(self.user.username, response.content)

    def test_get_users_detail(self):
        """
        Ensure that admin user can GET user-detail
        """
        url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.superuser.username, response.content)
        self.assertIn(self.superuser.first_name, response.content)
        self.assertIn(self.superuser.last_name, response.content)

    def test_get_users_detail_as_regular_user(self):
        """
        Ensure that regular user won't have access to GET user-detail
        """
        url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_detail_unauthorized(self):
        """
        Ensure that regular user won't have access to GET user-detail
        """
        url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_users_unauthorized(self):
        """
        Ensure that logged out users cannot POST
        """
        url = reverse('user-list')
        username = 'captobv'
        first_name = 'Captain'
        last_name = 'Obvious'
        email = 'captain@obvious.com'
        response = self.client.post(url, {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_users_regular_user(self):
        """
        Ensure that regular users cannot POST
        """
        url = reverse('user-list')
        self.client.force_authenticate(user=self.user)
        username = 'captobv'
        first_name = 'Captain'
        last_name = 'Obvious'
        email = 'captain@obvious.com'
        response = self.client.post(url, {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

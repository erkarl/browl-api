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
        # self.client.force_authenticate(user=self.user)
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

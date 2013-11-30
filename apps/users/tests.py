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

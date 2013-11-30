from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from django.contrib.auth.models import User
from rest_framework import status
# from django.test import TestCase


class UserTest(APITestCase):

    def setUp(self):
            self.apiclient = APIClient()
            self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'snow')
            self.factory = APIRequestFactory()

    def test_get_user_list_unauthorized(self):
        """
        Ensure that unauthorized users won't be able to GET user list
        """
        url = reverse('user-list')
        # response = self.client.get(url)
        request = self.factory.get(url, format='json')
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        import pdb
        pdb.set_trace()
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_as_admin(self):
        """
        Ensure that unauthorized users won't be able to GET user list
        """
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_FORBIDDEN)

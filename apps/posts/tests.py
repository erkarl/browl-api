from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from .models import Post
from rest_framework import status


class UserTest(APITestCase):

    def setUp(self):
            self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'snow')
            self.user = User.objects.create_user('tyrion', 'tyrion@lannister.com', 'lannister')
            self.post = Post(title='Random Title', body='Random Body', user=self.superuser)
            self.post.save()
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

    def test_post_update_unauthorized(self):
        """
        Ensure that logged out users cannot modify posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        user_url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        title = 'Random New Title'
        body = 'Random New Body'
        response = self.client.put(url, {'title': title, 'body': body, 'user': user_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_partial_update_unauthorized(self):
        """
        Ensure that logged out users cannot partially modify posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        title = 'Random New Title'
        response = self.client.patch(url, {'title': title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_partial_update_logged_in(self):
        """
        Ensure that regular users cannot partially modify posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        title = 'Random New Title'
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {'title': title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_partial_update_admin(self):
        """
        Ensure that admin users can partially modify posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        title = 'Random New Title Patched'
        user_url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(url, {'title': title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(title, response.content)
        self.assertIn(user_url, response.content)

    def test_post_update_regular_user(self):
        """
        Ensure that regular users cannot modify posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        user_url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        self.client.force_authenticate(user=self.user)
        title = 'Random New Title'
        body = 'Random New Body'
        response = self.client.put(url, {'title': title, 'body': body, 'user': user_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_update_admin(self):
        """
        Ensure that superusers can modify posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        user_url = reverse('user-detail', kwargs={'pk': self.superuser.id})
        self.client.force_authenticate(user=self.superuser)
        title = 'Random New Title'
        body = 'Random New Body'
        response = self.client.put(url, {'title': title, 'body': body, 'user': user_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(title, response.content)
        self.assertIn(body, response.content)
        self.assertIn(user_url, response.content)

    def test_post_delete_unauthorized(self):
        """
        Ensure that logged out users cannot delete posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_logged_in(self):
        """
        Ensure that regular users cannot delete posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_admin(self):
        """
        Ensure that admin users can delete posts
        """
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_head_unauthorized(self):
        """
        Ensure that unauthorized users can HEAD posts list
        """
        url = reverse('post-list')
        response = self.client.head(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_head_logged_in(self):
        """
        Ensure that logged in users can HEAD posts list
        """
        url = reverse('post-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.head(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_head_admin(self):
        """
        Ensure that admin users can HEAD posts list
        """
        url = reverse('post-list')
        self.client.force_authenticate(user=self.superuser)
        response = self.client.head(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_options_unauthorized(self):
        """
        Ensure that unauthorized users can OPTIONS posts list
        """
        url = reverse('post-list')
        response = self.client.options(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Post List', response.content)

    def test_post_options_logged_in(self):
        """
        Ensure that logged in users can OPTIONS posts list
        """
        url = reverse('post-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.options(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Post List', response.content)

    def test_post_options_admin(self):
        """
        Ensure that admin users can OPTIONS posts list
        """
        url = reverse('post-list')
        self.client.force_authenticate(user=self.superuser)
        response = self.client.options(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Post List', response.content)

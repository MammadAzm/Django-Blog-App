from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import json


class SignUpTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        pass

    def test_signup_successful(self):
        signup_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('signup')
        response = self.client.post(url, signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_invalid_data(self):
        invalid_data = {
            'username': None,
            'password': 'Jack1234',
        }

        url = reverse('signup')

        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_duplicate_username(self):
        signup_data = {
            'username': 'Sara',
            'password': 'Sara1234',
        }
        url = reverse('signup')
        response = self.client.post(url, signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="Jack",
            password=make_password("Jack1234"),
        )

        self.client = APIClient()

    def test_login_successful(self):
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password(self):
        invalid_data = {
            'username': "Jack",
            'password': 'WrongPassword',
        }

        url = reverse('login')

        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_data(self):
        invalid_data = {
            'username': None,
            'password': 'WrongPassword',
        }

        url = reverse('login')

        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        invalid_data = {
            'username': "Jack",
            'password': None,
        }

        url = reverse('login')

        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="Jack",
            password=make_password("Jack1234"),
        )

        self.client = APIClient()

    def test_logout_successful(self):
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = json.loads(response.content.decode('utf-8'))['token']

        url = reverse('logout')
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, login_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_invalid_credentials(self):
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = json.loads(response.content.decode('utf-8'))['token']
        url = reverse('logout')
        headers = {
            'Authorization': 'Token W3r4o3n1g1T8o8k5e8n0',
        }
        response = self.client.post(url, login_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreatePostTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="Jack",
            password=make_password("Jack1234"),
        )

        self.client = APIClient()

    def test_create_post_successful(self):
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('create_post')
        post_data = {
            'title': 'Huawei is on Fire',
            'content': 'Huawei have just released their latest Mate XS flagship smartphone with surprising adjustable screen size feature. Wait for updates...',
        }
        token = json.loads(response.content.decode('utf-8'))['token']
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_invalid_credentials(self):
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('create_post')
        post_data = {
            'title': 'Huawei is on Fire',
            'content': 'Huawei have just released their latest Mate XS flagship smartphone with surprising adjustable screen size feature. Wait for updates...',
        }
        token = "I5n6v7a9l06i4d33C3r3e3d3e5n7t8i90a946l5413s"
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetPostsTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="Jack",
            password=make_password("Jack1234"),
        )

        self.client = APIClient()

    def test_get_all_posts_successful(self):
        # First Create some Posts
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('create_post')
        token = json.loads(response.content.decode('utf-8'))['token']
        post_data = {
            'title': 'Huawei is on Fire',
            'content': 'Huawei have just released their latest Mate XS flagship smartphone with surprising adjustable screen size feature. Wait for updates...',
        }
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {
            'title': 'Samsung Stock Falldown',
            'content': 'Samsung market value is facing a massive drop due to the reports on Galaxy Note 7 explosions.',
        }

        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logout')
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, login_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('get_all_posts')
        response = self.client.get(url, format='json',)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_specific_post(self):
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('create_post')
        token = json.loads(response.content.decode('utf-8'))['token']
        post_data = {
            'title': 'Huawei is on Fire',
            'content': 'Huawei have just released their latest Mate XS flagship smartphone with surprising adjustable screen size feature. Wait for updates...',
        }
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {
            'title': 'Samsung Stock Falldown',
            'content': 'Samsung market value is facing a massive drop due to the reports on Galaxy Note 7 explosions.',
        }

        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logout')
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, login_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        valid_post_ids = [1, 2]
        invalid_post_ids = [100, 200]

        for post_id in valid_post_ids:
            url = reverse('get_post', args=[post_id])
            response = self.client.get(url, format='json',)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for post_id in invalid_post_ids:
            url = reverse('get_post', args=[post_id])
            response = self.client.get(url, format='json',)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostActionsTest(TestCase):
    def setUp(self):
        User.objects.create(
            username="Jack",
            password=make_password("Jack1234"),
        )
        User.objects.create(
            username="Sara",
            password=make_password("Sara1234"),
        )
        self.client = APIClient()

    def test_update_post_successful(self):
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('create_post')
        token = json.loads(response.content.decode('utf-8'))['token']
        post_data = {
            'title': 'Huawei is on Fire',
            'content': 'Huawei have just released their latest Mate XS flagship smartphone with surprising adjustable screen size feature. Wait for updates...',
        }
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {
            'title': 'Samsung Stock FallDown',
            'content': 'Samsung market value is facing a massive drop due to the reports on Galaxy Note 7 explosions.',
        }

        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logout')
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, login_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_data = {
            'username': 'Sara',
            'password': 'Sara1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('create_post')
        token = json.loads(response.content.decode('utf-8'))['token']
        post_data = {
            'title': 'Sara First Post',
            'content': 'Sara First Post Details',
        }
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {
            'title': 'Sara Second Post',
            'content': 'Sara Second Post Details',
        }

        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logout')
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, login_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content.decode('utf-8'))['token']

        post_id = 1
        edit_data = {
            'title': "New Title",
        }
        headers = {
            'Authorization': f'Token {token}',
        }
        url = reverse('update_post', args=[post_id])
        response = self.client.post(url, edit_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_id = 3
        edit_data = {
            'title': "New Title",
        }
        url = reverse('update_post', args=[post_id])
        response = self.client.post(url, edit_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_successful(self):
        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('create_post')
        token = json.loads(response.content.decode('utf-8'))['token']
        post_data = {
            'title': 'Huawei is on Fire',
            'content': 'Huawei have just released their latest Mate XS flagship smartphone with surprising adjustable screen size feature. Wait for updates...',
        }
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {
            'title': 'Samsung Stock FallDown',
            'content': 'Samsung market value is facing a massive drop due to the reports on Galaxy Note 7 explosions.',
        }

        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logout')
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, login_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_data = {
            'username': 'Sara',
            'password': 'Sara1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('create_post')
        token = json.loads(response.content.decode('utf-8'))['token']
        post_data = {
            'title': 'Sara First Post',
            'content': 'Sara First Post Details',
        }
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {
            'title': 'Sara Second Post',
            'content': 'Sara Second Post Details',
        }

        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, post_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('logout')
        headers = {
            'Authorization': f'Token {token}',
        }
        response = self.client.post(url, login_data, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_data = {
            'username': 'Jack',
            'password': 'Jack1234',
        }
        url = reverse('login')
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content.decode('utf-8'))['token']

        post_id = 1
        headers = {
            'Authorization': f'Token {token}',
        }
        url = reverse('delete_post', args=[post_id])
        response = self.client.post(url, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_id = 3
        url = reverse('delete_post', args=[post_id])
        response = self.client.post(url, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

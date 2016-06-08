from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class ApiTest(APITestCase):
    def setUp(self):
        self.maxDiff = None
        self.username = 'test'
        self.username2 = 'test2'

        self.password = 'P@ssW0rd123'
        self.password_equal = 'P@ssW0rd123'
        self.password_not_equal = 'P@ssW0rd1'

    def set_token(self, credentials):
        url = reverse('obtain_jwt_token')
        response = self.client.post(url, credentials)
        self.token = response.data.get("token")

    def test_create_user(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        self.assertTrue(get_user_model().objects.count(), 1)

    def test_do_not_create_user_when_there_are_not_username(self):
        user = {
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('username' in response.data)

    def test_do_not_create_user_when_there_are_not_password(self):
        user = {
            'username': self.username,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_do_not_create_user_when_there_are_not_confirm_password(self):
        user = {
            'username': self.username,
            'password': self.password,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_do_not_create_user_when_there_are_not_data(self):
        user = {}
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_do_not_create_user_when_password_and_confirm_password_are_not_equal(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_not_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_and_login(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        self.client.post(url, user)
        # login
        self.set_token({
            'username': self.username,
            'password': self.password,
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # check is login by getting his profile
        url = reverse('api:users-detail', args=[self.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)

    def test_do_not_login_if_user_is_not_active(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        self.client.post(url, user)
        # set not active
        user = get_user_model().objects.last()
        user.is_active = False
        user.save()

        url = reverse('obtain_jwt_token')
        response = self.client.post(url, {
            'username': self.username,
            'password': self.password,
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_and_do_not_get_user_if_not_login(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        url = reverse('api:users-detail', args=[user['username']])
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_and_get_another_user(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        user2 = {
            'username': self.username2,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user2['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        # check that exist 2 user
        self.assertTrue(get_user_model().objects.count(), 2)
        # login with user 1
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:users-detail', args=[user2['username']])
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user2['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)

    def test_create_user_and_do_not_get_others_users_if_not_login(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        user2 = {
            'username': self.username2,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user2['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        # check that exist 2 user
        self.assertTrue(get_user_model().objects.count(), 2)
        # login with user 1
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        url = reverse('api:users-detail', args=[user2['username']])
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_users_and_get_all_user(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        user2 = {
            'username': self.username2,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user2['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        # check that exist 2 user
        self.assertTrue(get_user_model().objects.count(), 2)
        # login with user 1
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:users-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_users_and_do_not_get_all_users_if_not_login(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        user2 = {
            'username': self.username2,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user2['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        # check that exist 2 user
        self.assertTrue(get_user_model().objects.count(), 2)
        # login with user 1
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        url = reverse('api:users-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_and_update(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:users-detail', args=[user['username']])
        # update user
        user['first_name'] = 'John'
        user['last_name'] = 'Doe'
        response = self.client.put(url, user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], user['first_name'])
        self.assertEqual(response.data['last_name'], user['last_name'])
        self.assertEqual(len(response.data['tasks']), 0)

    def test_create_user_and_do_not_update_if_not_login(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)

        url = reverse('api:users-detail', args=[user['username']])
        # update user
        user['first_name'] = 'John'
        user['last_name'] = 'Doe'
        response = self.client.put(url, user)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_and_update_password_re_login_with_new(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        # login
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:users-detail', args=[user['username']])
        # update user password
        user['password'] = 'P@ssW0rd123foo'
        user['confirm_password'] = 'P@ssW0rd123foo'
        response = self.client.put(url, user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # re-login with new password
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # get user with new password
        url = reverse('api:users-detail', args=[self.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)

    def test_create_user_and_do_not_update_password_when_confirm_is_not_equal(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        # login
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:users-detail', args=[user['username']])
        # update user password
        user['password'] = 'P@ssW0rd123foo'
        user['confirm_password'] = 'P@ssW0rd123faa'
        response = self.client.put(url, user)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        # login with old to check that don't change
        self.set_token({
            'username': user['username'],
            'password': self.password,
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # get user with current token
        url = reverse('api:users-detail', args=[self.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)

    def test_create_user_and_update_password_but_do_not_login_with_old_pass(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        # login
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:users-detail', args=[user['username']])
        # update user password
        user['password'] = 'P@ssW0rd123foo'
        user['confirm_password'] = 'P@ssW0rd123foo'
        response = self.client.put(url, user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # re-login with old password
        url = reverse('obtain_jwt_token')
        response = self.client.post(url, {
            'username': self.username,
            'password': self.password,
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_users_and_do_not_update_another_user(self):
        user = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        user2 = {
            'username': self.username2,
            'password': self.password,
            'confirm_password': self.password_equal,
        }
        url = reverse('api:users-list')
        response = self.client.post(url, user2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], user2['username'])
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')
        self.assertEqual(len(response.data['tasks']), 0)
        # check that exist 2 user
        self.assertTrue(get_user_model().objects.count(), 2)
        # login with user 1
        self.set_token({
            'username': user['username'],
            'password': user['password'],
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # try to update other user
        url = reverse('api:users-detail', args=[user2['username']])
        user['first_name'] = 'John'
        user['last_name'] = 'Doe'
        response = self.client.put(url, user)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

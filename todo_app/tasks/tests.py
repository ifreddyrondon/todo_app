from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


# Create your tests here.
class ApiTest(APITestCase):
    def setUp(self):
        self.maxDiff = None
        self.username = 'test'
        self.username2 = 'test2'
        self.password = 'P@ssW0rd123'

        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password)

        self.user_data = {
            'username': self.username,
            'password': self.password
        }

        self.user2 = get_user_model().objects.create_user(
            username=self.username2, password=self.password)

        self.user_data2 = {
            'username': self.username2,
            'password': self.password
        }

        self.set_token(self.user_data)

    def set_token(self, credentials):
        url = reverse('obtain_jwt_token')
        response = self.client.post(url, credentials)
        self.token = response.data.get("token")

    def test_authorization(self):
        url = reverse('obtain_jwt_token')
        response = self.client.post(url, self.user_data)
        self.assertNotEqual(response.data.get("token"), None)

    def test_create_simple_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        task = {
            'title': 'test_simple_task',
        }
        url = reverse('api:tasks-list')
        response = self.client.post(url, task)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['title'], task["title"])
        self.assertEqual(response.data['completed'], False)
        # check that task exist
        self.assertEquals(Task.objects.all().count(), 1)

    def test_do_not_create_task_is_not_title(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        task = {}
        url = reverse('api:tasks-list')
        response = self.client.post(url, task)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # check that tasks was not created
        self.assertEquals(Task.objects.all().count(), 0)

    def test_create_completed_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        task = {
            'title': 'test_simple_task',
            'completed': True
        }
        url = reverse('api:tasks-list')
        response = self.client.post(url, task)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['title'], task["title"])
        self.assertEqual(response.data['completed'], True)
        # check that task exist
        self.assertEquals(Task.objects.all().count(), 1)

    def test_create_task_and_get_their_status(self):
        self.set_token(self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:tasks-list')
        task = {
            'title': 'test_task',
        }
        task2 = {
            'title': 'test_task',
            'completed': True
        }
        # create tasks for user
        response = self.client.post(url, task)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, task2)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # check that exist two tasks
        self.assertEquals(Task.objects.all().count(), 2)
        # get tasks
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # # check their status
        self.assertEqual(response.data[0]['completed'], False)
        self.assertEqual(response.data[1]['completed'], True)

    def test_get_all_user_tasks_and_not_other_users_tasks(self):
        self.set_token(self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:tasks-list')
        task = {
            'title': 'test_task',
        }
        # create one task for fist user
        response = self.client.post(url, task)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # change user
        self.set_token(self.user_data2)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # check that exist one task
        self.assertEquals(Task.objects.all().count(), 1)
        # check tasks of new user, must be 0
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)
        # create task for new user
        response = self.client.post(url, task)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # now the user must have one task
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
        # check that exist two tasks
        self.assertEquals(Task.objects.all().count(), 2)

    def test_get_one_user_task_and_not_other_user_task(self):
        self.set_token(self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('api:tasks-list')
        task = {
            'title': 'test_task',
        }
        # create one task for fist user
        response = self.client.post(url, task)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # get new task id
        task_id_user1 = response.data['id']
        # get task detail
        url = reverse('api:tasks-detail', args=[task_id_user1])
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # change user
        self.set_token(self.user_data2)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # check that exist one task
        self.assertEquals(Task.objects.all().count(), 1)
        # get task detail of user1 with user2, response should be 404
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_task_as_completed(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        task = {
            'title': 'test_simple_task',
        }
        url = reverse('api:tasks-list')
        response = self.client.post(url, task)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['title'], task["title"])
        self.assertEqual(response.data['completed'], False)
        # get new task id
        task_id = response.data['id']
        url = reverse('api:tasks-detail', args=[task_id])
        # update task
        task['completed'] = True
        response = self.client.put(url, task)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['title'], task["title"])
        self.assertEqual(response.data['completed'], True)

    def test_mark_task_as_completed_with_partial_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        task = {
            'title': 'test_simple_task',
        }
        url = reverse('api:tasks-list')
        response = self.client.post(url, task)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['title'], task["title"])
        self.assertEqual(response.data['completed'], False)
        # get new task id
        task_id = response.data['id']
        url = reverse('api:tasks-detail', args=[task_id])
        # update task
        response = self.client.patch(url, {
            "completed": True
        })
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['title'], task["title"])
        self.assertEqual(response.data['completed'], True)

    def test_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        task = {
            'title': 'test_simple_task',
        }
        url = reverse('api:tasks-list')
        response = self.client.post(url, task)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['title'], task["title"])
        self.assertEqual(response.data['completed'], False)
        # check that exist one task
        self.assertEquals(Task.objects.all().count(), 1)
        # get new task id
        task_id = response.data['id']
        url = reverse('api:tasks-detail', args=[task_id])
        response = self.client.delete(url, task)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # check that still exist the place
        self.assertEquals(Task.objects.all().count(), 1)
        # but can't be reachable
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

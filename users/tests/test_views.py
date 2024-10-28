# users/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer
from users.repository import UserRepository
from datetime import date


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = UserRepository.create_user(
            name="John Doe", date_of_birth="1990-01-01"
        )
        self.user2 = UserRepository.create_user(
            name="Jane Smith", date_of_birth="1985-05-20"
        )

        # Store URLs for convenience
        self.list_url = reverse('user-list')
        self.detail_url = lambda pk: reverse('user-detail', args=[pk])

    def test_list_users(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
        serializer = UserSerializer([self.user2, self.user1], many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_list_users_pagination(self):
        # Create additional users to exceed page size
        for i in range(15):
            UserRepository.create_user(
                name=f"User {i}", date_of_birth="1990-01-01"
            )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Default page size
        self.assertIn('next', response.data)

    def test_retrieve_user(self):
        response = self.client.get(self.detail_url(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user1)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_nonexistent_user(self):
        response = self.client.get(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_create_user(self):
        data = {
            'name': 'Alice Johnson',
            'date_of_birth': '1992-07-15'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(User.objects.count(), 3)

    def test_create_user_invalid_data(self):
        data = {'name': '', 'date_of_birth': '1992-07-15'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_user(self):
        data = {'name': 'John Doe Updated', 'date_of_birth': '1990-01-01'}
        response = self.client.put(self.detail_url(self.user1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, data['name'])

    def test_update_nonexistent_user(self):
        data = {'name': 'Nonexistent User', 'date_of_birth': '1990-01-01'}
        response = self.client.put(self.detail_url(9999), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        response = self.client.delete(self.detail_url(self.user1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_delete_nonexistent_user(self):
        response = self.client.delete(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
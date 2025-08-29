from django.test import TestCase

# Creating testcase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserRegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "testuser",
            "password": "Pass1234!",
            "password2": "Pass1234!",
            "email": "test@example.com",
            "age": 15
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Pass1234!', age=15)

    def test_login(self):
        data = {
            "username": "testuser",
            "password": "Pass1234!"
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("'access', 'response.data'")



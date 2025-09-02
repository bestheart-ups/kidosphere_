# core/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class AuthTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("signup")
        self.login_url = reverse("login")
        self.token_refresh_url = reverse("token_refresh")
        self.protected_url = reverse("post-list-create")  # protected route

        self.user_data = {
            "username": "testuser",
            "password": "strongpassword123",
            "email": "testuser@example.com"
        }

        # Create user directly for login tests
        self.user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="password123"
        )

    def test_register_user(self):
        """User should be able to register"""
        response = self.client.post(self.register_url, self.user_data)
        print("REGISTER RESPONSE:", response.status_code, response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        """User should be able to login and get tokens"""
        response = self.client.post(self.login_url, {
            "username": "existinguser",
            "password": "password123"
        })
        print("LOGIN RESPONSE:", response.status_code, response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # save token for later
        self.access_token = response.data["access"]

    def test_protected_route_requires_auth(self):
        """Should block unauthenticated users"""
        response = self.client.get(self.protected_url)
        print("PROTECTED (NO TOKEN):", response.status_code, response.data)

        # Expect 401 Unauthorized (not 403)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_route_with_auth(self):
        """Should allow access with valid token"""
        login_response = self.client.post(self.login_url, {
            "username": "existinguser",
            "password": "password123"
        })
        token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.protected_url)
        print("PROTECTED (WITH TOKEN):", response.status_code, response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        """Should refresh token with valid refresh token"""
        login_response = self.client.post(self.login_url, {
            "username": "existinguser",
            "password": "password123"
        })
        refresh_token = login_response.data["refresh"]

        response = self.client.post(self.token_refresh_url, {
            "refresh": refresh_token
        })
        print("REFRESH RESPONSE:", response.status_code, response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

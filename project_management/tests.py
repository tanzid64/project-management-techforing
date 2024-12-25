from rest_framework.test import APITestCase
from rest_framework import status
from project_management.models import User
from project_management.serializers import UserRegistrationSerializer, UserSerializer
from typing import Dict


class UserRegistrationViewTestCase(APITestCase):
    """
    Test cases for User Registration View.
    """

    def test_user_registration_view(self):
        valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword",
            "confirm_password": "securepassword",
            "first_name": "test",
            "last_name": "user",
        }

        response = self.client.post("/api/users/register/", data=valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_registration_password_mismatch(self):
        """
        Test registration view fails when passwords don't match.
        """
        invalid_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword",
            "confirm_password": "differentpassword",
            "first_name": "New",
            "last_name": "User",
        }

        response = self.client.post("/api/users/register/", data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match", str(response.data))
        self.assertFalse(User.objects.filter(username="newuser").exists())


class UserLoginViewTestCase(APITestCase):
    """
    Test cases for User Login View.
    """

    def setUp(self):
        # Create a test user for login tests
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="securepassword"
        )
        self.login_url = "/api/users/login/"

    def test_user_login_success(self):
        data = {
            "email": "testuser@example.com",
            "password": "securepassword",
        }

        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "User logged in successfully")

    def test_user_login_invalid_credentials(self):
        data = {
            "email": "testuser@example.com",
            "password": "wrongpassword",
        }

        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Invalid email or password")

    def test_user_login_nonexistent_user(self):
        """
        Test login with an email that doesn't exist.
        """
        data = {
            "email": "nonexistent@example.com",
            "password": "securepassword",
        }

        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Invalid email or password")

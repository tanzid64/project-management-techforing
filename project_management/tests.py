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

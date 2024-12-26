from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()


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


class UserGetUpdateDeleteViewTestCase(APITestCase):
    """
    Test cases for UserGetUpdateDeleteView.
    """

    def setUp(self):
        # Create users for testing
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="securepassword1"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="securepassword2"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword"
        )

        self.user1_url = reverse("user-get-update-delete", kwargs={"pk": self.user1.id})
        self.user2_url = reverse("user-get-update-delete", kwargs={"pk": self.user2.id})

    def test_get_user_details_authenticated(self):
        """
        Test retrieving user details as an authenticated user.
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.user1_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user1.username)

    def test_update_user_details_self(self):
        """
        Test updating user details by the user themselves.
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(
            self.user1_url,
            data={
                "username": "updateduser1",
                "email": "updateduser1@example.com",
                "password": "newpassword1",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "updateduser1")
        self.assertEqual(self.user1.email, "updateduser1@example.com")

    def test_update_user_details_unauthorized(self):
        """
        Test updating another user's details (not admin).
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(
            self.user2_url,
            data={
                "username": "unauthorizedupdate",
                "email": "unauthorized@example.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_user(self):
        """
        Test updating user details as an admin.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            self.user1_url,
            data={
                "username": "adminupdateduser1",
                "email": "adminupdateduser1@example.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "adminupdateduser1")

    def test_delete_user_self(self):
        """
        Test deleting user account by the user themselves.
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.user1_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_delete_user_unauthorized(self):
        """
        Test deleting another user's account (not admin).
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.user2_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_any_user(self):
        """
        Test deleting user account as an admin.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.user1_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

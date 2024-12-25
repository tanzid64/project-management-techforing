from django.contrib.auth.models import BaseUserManager
from typing import Optional
from django.db.models import Model


class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for authentication instead of usernames.
    """

    def create_user(
        self, email: str, password: str, confirm_password: Optional[str] = None, **extra_fields
    ) -> Model:
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields
    ) -> Model:
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

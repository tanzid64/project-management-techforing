from typing import Dict
from rest_framework_simplejwt.tokens import RefreshToken
from project_management.models import User


def get_tokens_for_user(user: User) -> Dict[str, str]:
    """
    Get refresh and access tokens for a user
    :param user: User object
    :return: Dictionary containing refresh and access tokens
    """

    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

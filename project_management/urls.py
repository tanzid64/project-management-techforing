from django.urls import path
from project_management.views import (
    UserRegistrationView,
    UserLoginView,
    UserGetUpdateDeleteView,
)

urlpatterns = [
    # User paths:-
    path("users/register/", UserRegistrationView.as_view(), name="register"),
    path("users/login/", UserLoginView.as_view(), name="login"),
    path("users/<int:pk>/", UserGetUpdateDeleteView.as_view(), name="user-get-update-delete"),
]

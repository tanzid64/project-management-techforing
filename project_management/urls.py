from django.urls import path, include
from rest_framework import routers
from project_management.views import (
    UserRegistrationView,
    UserLoginView,
    UserGetUpdateDeleteView,
    ProjectViewSet,
)

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet)

urlpatterns = [
    # User paths:-
    path("users/register/", UserRegistrationView.as_view(), name="register"),
    path("users/login/", UserLoginView.as_view(), name="login"),
    path("users/<int:pk>/", UserGetUpdateDeleteView.as_view(), name="user-get-update-delete"),
    # Project paths:-
    path("", include(router.urls)),
]

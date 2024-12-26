from django.urls import path, include
from rest_framework import routers
from project_management.views import (
    UserRegistrationView,
    UserLoginView,
    UserGetUpdateDeleteView,
    ProjectViewSet,
    TaskViewSet,
    CommentViewSet,
)

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet)

# TaskViewSet URLs
task_list_create_view = TaskViewSet.as_view({"get": "list", "post": "create"})
task_detail_view = TaskViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

# CommentViewSet URLs
comment_list_create_view = CommentViewSet.as_view({"get": "list", "post": "create"})
comment_detail_view = CommentViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    # User paths:-
    path("users/register/", UserRegistrationView.as_view(), name="register"),
    path("users/login/", UserLoginView.as_view(), name="login"),
    path(
        "users/<int:pk>/",
        UserGetUpdateDeleteView.as_view(),
        name="user-get-update-delete",
    ),
    # Project paths:-
    path("", include(router.urls)),
    # Task paths:-
    path(
        "projects/<int:project_id>/tasks/",
        task_list_create_view,
        name="task-list-create",
    ),
    path(
        "tasks/<int:pk>/",
        task_detail_view,
        name="task-detail",
    ),
    # Comment paths:-
    path(
        "tasks/<int:task_id>/comments/",
        comment_list_create_view,
        name="comment-list-create",
    ),
    path(
        "comments/<int:pk>/",
        comment_detail_view,
        name="comment-detail",
    ),
]

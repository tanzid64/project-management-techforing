# Django Imports
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied

# Project Management Imports
from project_management.helpers import get_tokens_for_user
from project_management.models import Comment, Project, Task
from project_management.permissions import CommentPermission, TaskPermission, ProjectPermission
from project_management.serializers import (
    CommentSerializer,
    ProjectSerializer,
    TaskSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserRegistrationSerializer,
)


User = get_user_model()


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    """
    View for registering a new user
    """

    serializer_class = UserRegistrationSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
            refresh_token_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
            return Response(
                {
                    "success": True,
                    "message": "User registered successfully",
                    "tokens": tokens,
                    "expires_in": {
                        "access": access_token_lifetime.total_seconds(),
                        "refresh": refresh_token_lifetime.total_seconds(),
                    },
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    View for logging in a user
    """

    serializer_class = UserLoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(email=email, password=password)
        if user is None:
            return Response(
                {"success": False, "message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        tokens = get_tokens_for_user(user)
        access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        refresh_token_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
        return Response(
            {
                "success": True,
                "message": "User logged in successfully",
                "tokens": tokens,
                "expires_in": {
                    "access": access_token_lifetime.total_seconds(),
                    "refresh": refresh_token_lifetime.total_seconds(),
                },
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

class UserGetUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for get, update and delete an user.
    Permissions: Any authenticated user can make a get request. For other request user can only make request on their own id. Admin can do everything.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj: User = super().get_object()

        # Restrict update/delete to the user themselves or an admin
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            if not self.request.user.is_superuser and obj != self.request.user:
                raise PermissionDenied(
                    "You do not have permission to modify this user."
                )
        return obj


class ProjectViewSet(viewsets.ModelViewSet):
    """
    View for get, create, update and delete a project.
    Permissions: Any authenticated user can make a get request. For other request user can only make request if they are the owner. Admin can do everything.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ProjectPermission]

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]

    def get_queryset(self):
        if "project_id" in self.kwargs:
            project = Project.objects.get(id=self.kwargs["project_id"])
            return Task.objects.filter(project=project)
        return Task.objects.all()

    def create(self, request: Request, *args, **kwargs) -> Response:
        project = Project.objects.get(id=self.kwargs["project_id"])
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data)
        return Response(serializer.errors)


class CommentViewSet(viewsets.ModelViewSet):
    """
    View for get, create, update and delete a comment.
    Permissions: Any user can make a get request. For other request user can only make request if they are the owner, commenter or admin. Admin can do everything.
    """
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def get_queryset(self):
        if "task_id" in self.kwargs:
            task = Task.objects.get(id=self.kwargs["task_id"])
            return Comment.objects.filter(task=task)
        return Comment.objects.all()

    def create(self, request: Request, *args, **kwargs) -> Response:
        # Get the task based on the task_id in the URL
        task = Task.objects.get(id=self.kwargs["task_id"])
        user = request.user

        # Ensure the task and user are included in the serializer data
        serializer_data = request.data.copy()
        serializer_data["task"] = task.id  # Add task to the data
        serializer_data["user"] = user.id  # Add user to the data

        # Serialize the data
        serializer = self.get_serializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save(task=task, user=user)  # Save the comment with task and user
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

from functools import partial
from rest_framework.views import APIView
from project_management.helpers import get_tokens_for_user
from project_management.models import Comment, Project, Task
from project_management.permissions import IsOwnerOrAdminOnly
from project_management.renderers import UserRenderer
from project_management.serializers import (
    CommentSerializer,
    ProjectSerializer,
    TaskSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserRegistrationSerializer,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import extend_schema, OpenApiExample

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
            return Response(
                {
                    "success": True,
                    "message": "User registered successfully",
                    "tokens": tokens,
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
        serializer = self.get_serializer(data=request.data)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(email=email, password=password)
        if user is None:
            return Response(
                {"success": False, "message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        tokens = get_tokens_for_user(user)
        return Response(
            {
                "success": True,
                "message": "User logged in successfully",
                "tokens": tokens,
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOnly]

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
    serializer_class = CommentSerializer

    def get_queryset(self):
        if "task_id" in self.kwargs:
            task = Task.objects.get(id=self.kwargs["task_id"])
            return Comment.objects.filter(task=task)
        return Comment.objects.all()

    def create(self, request: Request, *args, **kwargs) -> Response:
        task = Task.objects.get(id=self.kwargs["task_id"])
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, user=user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

from rest_framework.views import APIView
from project_management.helpers import get_tokens_for_user
from project_management.serializers import UserSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate, get_user_model

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

    def post(self, request: Request) -> Response:
        email = request.data.get("email")
        password = request.data.get("password")
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

    def get_object(self) -> User:
        obj: User = super().get_object()

        # Restrict update/delete to the user themselves or an admin
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            if not self.request.user.is_superuser and obj != self.request.user:
                raise PermissionDenied(
                    "You do not have permission to modify this user."
                )
        return obj

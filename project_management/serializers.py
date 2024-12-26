from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import get_user_model
from project_management.models import Project, Task

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User.
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "date_joined")
        read_only_fields = ("date_joined", "id")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for User Registration. Password is write only field.
    """

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
        )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserForProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for User for Project.
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project.
    """

    owner = UserForProjectSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "created_at", "updated_at", "owner")
        read_only_fields = ("created_at", "updated_at", "id")


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task.
    """

    assign_to = UserForProjectSerializer(source="assigned_to", read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "assigned_to",
            "status",
            "priority",
            "due_date",
            "created_at",
            "project",
            "assign_to",
        )
        read_only_fields = ("created_at", "id")
        
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment.
    """

    class Meta:
        model = Task
        fields = (
            "id",
            "content",
            "created_at",
            "user",
            "task",
        )
        read_only_fields = ("created_at", "id")

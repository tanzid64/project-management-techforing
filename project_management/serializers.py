from typing import Any, Dict
from rest_framework import serializers
from project_management.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model. Password is write only field.
    """

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "date_joined",
        )
        read_only_fields = ("date_joined", "id")
        
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data) -> User:
        user = User.objects.create_user(**validated_data)
        return user

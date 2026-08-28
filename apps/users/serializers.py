from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for exposing non-sensitive user profile data."""

    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "date_joined")
        read_only_fields = ("id", "role", "date_joined")


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for handling new user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        # set_password ensures PBKDF2 hashing before saving to DB
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=User.Role.CLIENT,  # New registrations default to CLIENT
        )
        return user

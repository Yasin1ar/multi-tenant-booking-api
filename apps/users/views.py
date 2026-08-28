from rest_framework import generics, permissions
from apps.users.models import User
from apps.users.serializers import UserRegisterSerializer, UserSerializer


class UserRegisterView(generics.CreateAPIView):
    """POST /api/v1/auth/register/ - Public endpoint for user registration."""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    """GET /api/v1/auth/me/ - Protected endpoint to get current authenticated user profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

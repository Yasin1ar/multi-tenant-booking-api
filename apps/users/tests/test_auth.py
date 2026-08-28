import pytest
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework import status

from apps.users.factories import UserFactory
from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:
    """Tests for the Custom User Model logic."""

    def test_create_user_with_default_role(self):
        user = UserFactory()
        assert user.role == User.Role.CLIENT
        assert user.check_password("defaultpassword123")

    def test_create_admin_role(self):
        user = UserFactory(role=User.Role.ADMIN)
        assert user.role == User.Role.ADMIN
        assert user.role == "ADMIN"

    def test_two_users_with_same_email_raise_error(self):
        """Verify that creating two users with the same email raises IntegrityError."""
        email = "dupyasin@gmail.com"
        user1 = UserFactory(email=email)
        with pytest.raises(IntegrityError):
            user2 = UserFactory(email=email)


@pytest.mark.django_db
class TestJWTAuthentication:
    """Tests for SimpleJWT auth endpoints (/api/v1/auth/token/)."""

    def test_obtain_token_success(self, client):
        user = UserFactory(username="testuser", password="securepassword123")
        url = reverse("token_obtain_pair")

        payload = {
            "username": "testuser",
            "password": "securepassword123",
        }

        response = client.post(url, data=payload, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.json()
        assert "refresh" in response.json()

    def test_obtain_token_invalid_credentials(self, client):
        UserFactory(username="testuser", password="securepassword123")
        url = reverse("token_obtain_pair")

        payload = {
            "username": "testuser",
            "password": "wrongpassword",
        }

        response = client.post(url, data=payload, content_type="application/json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "access" not in response.json()

    def test_refresh_token_success(self, client):
        user = UserFactory(username="testuser", password="securepassword123")
        token_url = reverse("token_obtain_pair")
        refresh_url = reverse("token_refresh")

        # 1. Login to get tokens
        token_response = client.post(
            token_url,
            data={"username": "testuser", "password": "securepassword123"},
            content_type="application/json",
        )
        refresh_token = token_response.json()["refresh"]

        # 2. Refresh token
        refresh_response = client.post(
            refresh_url,
            data={"refresh": refresh_token},
            content_type="application/json",
        )

        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access" in refresh_response.json()

    def test_unauthenticated_request_with_invalid_token(self, client):
        refresh_url = reverse("token_refresh")

        response = client.post(
            refresh_url,
            data={"refresh": "invalid_token_xyz"},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["code"] == "token_not_valid"

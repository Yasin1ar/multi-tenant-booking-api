import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.bookings.factories import BookingFactory
from apps.users.factories import UserFactory


@pytest.mark.django_db
class TestBookingAPI:
    """Integration tests for Booking endpoints and permissions."""

    def test_unauthenticated_request_fails(self):
        client = APIClient()
        url = reverse(
            "booking_detail", kwargs={"pk": "00000000-0000-0000-0000-000000000000"}
        )
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_can_retrieve_own_booking(self):
        client = APIClient()
        user = UserFactory()
        booking = BookingFactory(user=user)
        url = reverse("booking_detail", kwargs={"pk": booking.id})

        client.force_authenticate(user=user)
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == str(booking.id)

    def test_user_cannot_retrieve_other_user_booking(self):
        client = APIClient()
        user_a = UserFactory()
        user_b = UserFactory()
        booking_b = BookingFactory(user=user_b)
        url = reverse("booking_detail", kwargs={"pk": booking_b.id})

        client.force_authenticate(user=user_a)
        response = client.get(url)

        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]

from datetime import timedelta
import pytest
from django.db.utils import IntegrityError
from django.utils import timezone

from apps.bookings.models import Booking
from apps.organizations.factories import ResourceFactory
from apps.users.factories import UserFactory


@pytest.mark.django_db
def test_booking_end_time_before_start_time_fails():
    """Attempt to create a booking where end_time is BEFORE start_time"""
    user = UserFactory()
    resource = ResourceFactory()
    now = timezone.now()

    with pytest.raises(IntegrityError):
        Booking.objects.create(
            user=user,
            resource=resource,
            start_time=now,
            end_time=now - timedelta(hours=1),  # Invalid!
        )

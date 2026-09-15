from datetime import timedelta
import factory
from django.utils import timezone

from apps.bookings.models import Booking
from apps.organizations.factories import ResourceFactory
from apps.users.factories import UserFactory


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    user = factory.SubFactory(UserFactory)
    resource = factory.SubFactory(ResourceFactory)
    start_time = factory.LazyFunction(timezone.now)
    end_time = factory.LazyAttribute(lambda o: o.start_time + timedelta(hours=2))
    total_price = 50.00

from rest_framework import generics, permissions
from apps.bookings.models import Booking
from apps.bookings.permissions import IsBookingOwner
from apps.bookings.serializers import BookingSerializer


class BookingListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/bookings/ -> List user's bookings (or all if ADMIN)
    POST /api/v1/bookings/ -> Create a new booking
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "ADMIN":
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        # Automatically bind the authenticated user to the new booking
        serializer.save(user=self.request.user)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/bookings/<uuid:pk>/ -> Retrieve booking details
    PUT    /api/v1/bookings/<uuid:pk>/ -> Update booking
    DELETE /api/v1/bookings/<uuid:pk>/ -> Cancel/Delete booking
    """

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwner]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "ADMIN":
            return Booking.objects.all()
        return Booking.objects.filter(user=user)
from django.urls import path
from apps.bookings.views import BookingDetailView

urlpatterns = [
    path("<uuid:pk>/", BookingDetailView.as_view(), name="booking_detail"),
]
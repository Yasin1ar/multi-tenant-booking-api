from django.urls import path
from apps.bookings.views import BookingDetailView, BookingListCreateView

urlpatterns = [
    path("", BookingListCreateView.as_view(), name="booking_list_create"),
    path("<uuid:pk>/", BookingDetailView.as_view(), name="booking_detail"),
]
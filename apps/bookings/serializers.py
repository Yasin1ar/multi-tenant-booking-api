from rest_framework import serializers
from django.utils import timezone
from apps.bookings.models import Booking
from apps.organizations.models import Resource
from apps.users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for reading and creating Booking instances."""

    # Nested read-only fields for richer response payloads
    user = UserSerializer(read_only=True)
    resource_id = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.all(),
        source="resource",
        write_only=True,
    )

    class Meta:
        model = Booking
        fields = (
            "id",
            "resource",
            "resource_id",
            "user",
            "start_time",
            "end_time",
            "status",
            "total_price",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "resource",
            "user",
            "status",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        """Validate timing constraints at the application layer."""
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                {"end_time": "End time must be strictly after start time."}
            )

        if start_time and start_time < timezone.now():
            raise serializers.ValidationError(
                {"start_time": "Booking start time cannot be in the past."}
            )

        return attrs

    def create(self, validated_data):
        """Automatically assign the authenticated user making the request."""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)
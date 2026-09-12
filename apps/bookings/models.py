import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q, F
from apps.organizations.models import Resource


class Booking(models.Model):
    """Represents a scheduled reservation for a Resource by a User."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="bookings",
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        db_index=True,
    )

    # Timing & Status
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    
    # Financial tracking
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]
        constraints = [
            # Enforce start_time < end_time directly inside DB
            models.CheckConstraint(
                condition=Q(start_time__lt=F("end_time")),
                name="booking_start_time_before_end_time",
            )
        ]

    def __str__(self):
        return f"Booking {self.id} | {self.resource.name} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
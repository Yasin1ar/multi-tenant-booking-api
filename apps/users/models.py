from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        CLIENT = "CLIENT", "Client"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    REQUIRED_FIELDS = [
        "email",
        "role",
    ]  # Note for myself: It affects only the python manage.py createsuperuser command in your terminal. AbstractUser already requires username and password by default. Adding "email" and "role" to REQUIRED_FIELDS forces the interactive terminal prompt to ask for those two extra fields when creating an admin.

    def __str__(self):
        return f"{self.username} ({self.role})"

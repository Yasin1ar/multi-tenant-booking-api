from rest_framework import serializers
from apps.organizations.models import Organization, Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = (
            "id",
            "organization",
            "name",
            "description",
            "capacity",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class OrganizationSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "is_active",
            "resources",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

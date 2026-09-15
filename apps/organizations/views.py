from rest_framework import generics, permissions
from apps.organizations.models import Organization, Resource
from apps.organizations.serializers import OrganizationSerializer, ResourceSerializer
from apps.bookings.permissions import IsOrganizationAdmin


class OrganizationListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/organizations/     -> List all organizations
    POST /api/v1/organizations/     -> Create a new organization
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationAdmin]


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/organizations/<slug>/ -> Retrieve an organization by slug
    PUT    /api/v1/organizations/<slug>/ -> Update an organization
    DELETE /api/v1/organizations/<slug>/ -> Delete an organization
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationAdmin]
    lookup_field = "slug"


# --- Resource Views ---


class ResourceListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/resources/     -> List all bookable resources
    POST /api/v1/resources/     -> Create a new resource
    """

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationAdmin]

    def get_queryset(self):
        """Optionally filter resources by organization if provided in query parameters."""
        queryset = Resource.objects.all()
        org_id = self.request.query_params.get("organization")
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        return queryset


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/resources/<uuid:pk>/ -> Retrieve a specific resource
    PUT    /api/v1/resources/<uuid:pk>/ -> Update a resource
    DELETE /api/v1/resources/<uuid:pk>/ -> Delete a resource
    """

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationAdmin]

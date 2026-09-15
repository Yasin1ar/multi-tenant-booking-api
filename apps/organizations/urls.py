from django.urls import path
from apps.organizations.views import (
    OrganizationListCreateView,
    OrganizationDetailView,
    ResourceListCreateView,
    ResourceDetailView,
)

urlpatterns = [
    # Organization routes
    path(
        "organizations/",
        OrganizationListCreateView.as_view(),
        name="organization_list_create",
    ),
    path(
        "organizations/<slug:slug>/",
        OrganizationDetailView.as_view(),
        name="organization_detail",
    ),
    # Resource routes
    path(
        "resources/",
        ResourceListCreateView.as_view(),
        name="resource_list_create",
    ),
    path(
        "resources/<uuid:pk>/",
        ResourceDetailView.as_view(),
        name="resource_detail",
    ),
]

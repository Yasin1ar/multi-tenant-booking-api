import factory
from apps.organizations.models import Organization, Resource


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"Organization {n}")
    slug = factory.Sequence(lambda n: f"org-{n}")


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource

    organization = factory.SubFactory(OrganizationFactory)
    name = factory.Sequence(lambda n: f"Resource {n}")
    capacity = 10
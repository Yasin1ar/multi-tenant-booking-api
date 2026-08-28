import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
    role = User.Role.CLIENT

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override _create to ensure Django hashes the password correctly."""
        password = kwargs.pop("password", "defaultpassword123")
        user = super()._create(model_class, *args, **kwargs)
        user.set_password(password)
        user.save()
        return user

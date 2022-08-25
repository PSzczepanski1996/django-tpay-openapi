"""Create test transaction."""
# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _

# 3rd-party
import factory.fuzzy
from factory.django import DjangoModelFactory

# Project
from tpay_module.tpay_api import TPayModule


class UserFactory(DjangoModelFactory):
    """User factory class."""

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(
        lambda obj: '{0}@{1}'.format(
            obj.username,
            'gmail.com',
        ),
    )
    is_staff = False
    password = factory.LazyAttribute(lambda obj: '{0}'.format(make_password(obj.username)))

    class Meta:  # noqa: D106
        model = get_user_model()
        django_get_or_create = ('username',)


class Command(BaseCommand):
    """Command class."""

    help = 'Create test transaction for TPay.'

    def add_arguments(self, parser):  # noqa: D102
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        """Handle command."""
        tpay = TPayModule()
        user = UserFactory()
        response = tpay.create_transaction(
            user,
            0.01,
            email=options['email'],
        )
        if response:
            self.stdout.write(self.style.SUCCESS(
                    _('Created test transaction!'),
                ),
            )
            print('RESPONSE DATA:')
            print(response)
        else:
            self.stdout.write(self.style.ERROR(
                    _('The transaction creation failed!'),
                ),
            )

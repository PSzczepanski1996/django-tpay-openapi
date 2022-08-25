"""Create test transaction."""
# Django
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _

# Project
from tpay_module.tests.factories import UserFactory
from tpay_module.tpay_api import TPayModule


class UserCreationFactory(UserFactory):
    """User creation factory class."""

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

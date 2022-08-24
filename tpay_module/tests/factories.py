"""Factories generation file."""
# 3rd-party
import factory.fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

# Project
from tpay_module.models import SavedTPayCard
from tpay_module.models import TPayPayment
from tpay_module.models import TPaySettings
from tpay_module.tests.utils import MoneyProvider

faker = Faker()
faker.add_provider(MoneyProvider)


class TPayPaymentFactory(DjangoModelFactory):
    """Factory for payment model."""

    number = factory.Faker('uuid4')
    price = faker.money()
    email = factory.Faker('email')
    transaction_id = factory.Sequence(lambda n: n)

    class Meta:  # noqa: D106
        model = TPayPayment


class SavedTPayCardFactory(DjangoModelFactory):
    """Saved payment card model."""

    card_token = factory.fuzzy.FuzzyText(length=64)
    card_expiration_code = factory.fuzzy.FuzzyText(length=4)

    class Meta:  # noqa: D106
        model = SavedTPayCard


class TPaySettingsFactory(DjangoModelFactory):
    """TPay Settings factory."""

    return_url = factory.fuzzy.FuzzyText(length=255)
    client_id = factory.fuzzy.FuzzyText(length=255)
    client_secret = factory.fuzzy.FuzzyText(length=255)

    class Meta:  # noqa: D106
        model = TPaySettings

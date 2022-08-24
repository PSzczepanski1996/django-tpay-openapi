"""Test utils file."""
# Standard Library
import random

# 3rd-party
from djmoney.money import Money
from faker.providers import BaseProvider


class MoneyProvider(BaseProvider):
    """Money provider for custom money field django implementation."""

    def money(self):
        """Return random PLN value."""
        value = round(random.uniform(1, 100), 2)
        return Money(value, 'PLN')

"""Test models file."""
# Django
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

# Project
from tpay_module.tests.factories import SavedTPayCardFactory
from tpay_module.tests.factories import TPayPaymentFactory
from tpay_module.tests.factories import TPaySettingsFactory


class TestModels(TestCase):
    """Test models class."""

    def setUp(self) -> None:  # noqa: D102
        pass

    def test_tpay_payment_str_repr(self):
        """Test TPay payment string representation."""
        payment = TPayPaymentFactory()
        test_result = _('Transaction {0}').format(payment.number)
        self.assertEqual(payment.__str__(), test_result)

    def test_saved_tpay_card_str_repr(self):
        """Test saved tpay card model string representation."""
        card = SavedTPayCardFactory()
        test_result = _('Saved TPay Card ({0})').format(card.id)
        self.assertEqual(card.__str__(), test_result)

    def test_tpay_settings_str_repr(self):
        """Test tpay settings str repr."""
        settings = TPaySettingsFactory()
        test_result = _('TPay Settings')
        self.assertEqual(settings.__str__(), test_result)

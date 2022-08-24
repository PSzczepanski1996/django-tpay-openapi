"""Test tags functionality."""
# Django
from django.test import TestCase

# Project
from tpay_module.templatetags.tpay_tags import get_tpay_payment
from tpay_module.tests.factories import TPayPaymentFactory


class TestTags(TestCase):
    """Test tags functionality."""

    def setUp(self) -> None:  # noqa: D102
        pass

    def test_get_tpay_payment(self):
        """Test get tpay payment template tag."""
        payment = get_tpay_payment('XYZ123')
        self.assertEqual(payment, None)
        payment = TPayPaymentFactory(
            transaction_id='test1234',
        )
        test_result = get_tpay_payment('test1234')
        self.assertEqual(payment, test_result)

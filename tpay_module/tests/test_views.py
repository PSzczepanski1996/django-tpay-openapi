"""Test TPay views."""
# Django
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse


class TestViews(TestCase):
    """Test TPay views."""

    def setUp(self) -> None:  # noqa: D102
        pass

    def test_tpay_ipn_handler_get(self):
        """Test TPay IPN handler on get method callback."""
        url = reverse('tpay_ipn')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @override_settings(TPAY_DISABLE=True)
    def test_tpay_ipn_handler_post_disabled(self):
        """Test TPay IPN handler on post method callback when settings are disabled."""
        url = reverse('tpay_ipn')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

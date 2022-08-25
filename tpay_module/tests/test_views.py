"""Test TPay views."""
# Standard Library
import cgi
import hashlib
import random
import string

# Django
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

# Project
from tpay_module.forms import TPayIPNForm
from tpay_module.tests.factories import TPayPaymentFactory


class TestViews(TestCase):
    """Test TPay views."""

    def setUp(self) -> None:  # noqa: D102
        pass

    @staticmethod
    def get_random_string(length=0):  # noqa: D102
        if not length:
            return ''
        result_list = []
        for _ in range(length):
            result_list.append(random.choice(string.ascii_uppercase + string.digits))
        return ''.join(result_list)

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

    @override_settings(TPAY_SECURE_CODE='')
    def test_tpay_ipn_handler_no_secure_code(self):  # noqa: D102
        url = reverse('tpay_ipn')
        payment = TPayPaymentFactory()
        response = self.client.post(url, data={
            'tr_crc': payment.number,
            'id': self.get_random_string(64),
            'tr_id': self.get_random_string(64),
            'tr_paid': 0.01,
            'tr_status': TPayIPNForm.SUCCESS_STATUS,
        })
        charset = cgi.parse_header(
            response.headers['Content-Type'])[1]['charset']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(charset), 'FALSE')

    @override_settings(TPAY_SECURE_CODE='demo')
    def test_tpay_ipn_handler_wrong_md5(self):  # noqa: D102
        url = reverse('tpay_ipn')
        data_id = random.randint(1000000000, 9999999999)
        data_tr_id = random.randint(1000000000, 9999999999)
        md5sum = 'random_string'
        payment = TPayPaymentFactory()
        response = self.client.post(url, data={
            'tr_crc': payment.number,
            'id': data_id,
            'tr_id': data_tr_id,
            'tr_paid': payment.price.amount,
            'tr_status': TPayIPNForm.SUCCESS_STATUS,
            'md5sum': md5sum,
        })
        charset = cgi.parse_header(
            response.headers['Content-Type'])[1]['charset']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(charset), 'FALSE')

    @override_settings(TPAY_SECURE_CODE='demo')
    def test_tpay_ipn_request_successful(self):
        """Test tpay ipn if request is empty."""
        url = reverse('tpay_ipn')
        payment = TPayPaymentFactory()
        get_price = '{:.2f}'.format(payment.price.amount)  # noqa: P101
        payment_part = f'{get_price}{payment.number}'
        data_id = random.randint(1000000000, 9999999999)
        data_tr_id = random.randint(1000000000, 9999999999)
        secure_code = 'demo'
        md5sum = hashlib.md5(
            f'{data_id}{data_tr_id}{payment_part}{secure_code}'.encode('utf-8'),
        ).hexdigest()
        response = self.client.post(url, data={
            'id': data_id,
            'tr_id': data_tr_id,
            'tr_crc': payment.number,
            'tr_paid': get_price,
            'tr_status': TPayIPNForm.SUCCESS_STATUS,
            'md5sum': md5sum,
        })
        charset = cgi.parse_header(
            response.headers['Content-Type'])[1]['charset']
        self.assertEqual(response.status_code, 200)
        payment.refresh_from_db()
        self.assertTrue(payment.is_finished)
        self.assertEqual(response.content.decode(charset), 'TRUE')

"""Test APIs file."""
# Standard Library
import random
from datetime import datetime
from unittest.mock import Mock
from unittest.mock import patch

# Django
from django.http import Http404
from django.test import TestCase
from django.test import override_settings
from django.utils.translation import gettext_lazy as _

# 3rd-party
import pytest
from djmoney.money import Money

# Project
from tpay_module.models import TPayPayment
from tpay_module.tests.factories import UserFactory
from tpay_module.tpay_api import TPayModule
from tpay_module.utils import get_parsed_tpay_groups
from tpay_module.utils import get_tpay_groups


class TestTPayModule(TestCase):
    """Test TPay Module."""

    def setUp(self):
        """Set up init data."""
        self.module = TPayModule()

        class NopeStringObject(object):
            """Nope string object."""

            def __str__(self):  # noqa: D102
                raise NotImplementedError('You shall not pass!')

        self.nope_string_class = NopeStringObject
        self.bearer_token = 'test_bearer_token'
        self.tester_email = 'p.szczepanski996@gmail.com'

    @override_settings(TPAY_CLIENT_ID=None)
    @override_settings(TPAY_CLIENT_SECRET=None)
    def test_get_headers_404(self):
        """Test get headers method when it raises 404."""
        with pytest.raises(Exception) as exc_info:
            self.module.get_headers()
        self.assertEqual(type(exc_info.value), Http404)

    @override_settings(TPAY_CLIENT_ID='1010')
    @override_settings(TPAY_CLIENT_SECRET='demo')
    @patch('requests.post')
    def test_get_headers_simply(self, mock):
        """Test by simple way get headers method."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {'access_token': self.bearer_token},
        )
        headers = self.module.get_headers()
        self.assertEqual(
            headers,
            {'Authorization': f'Bearer {self.bearer_token}'},
        )

    @override_settings(TPAY_CLIENT_ID='1010')
    @override_settings(TPAY_CLIENT_SECRET='demo')
    @patch('requests.post')
    def test_get_headers_when_different_than_200(self, mock):
        """Test raise Http404 when TPay response code is other than 200."""
        mock.return_value = Mock(
            status_code=201,
            json=lambda: {'access_token': self.bearer_token},
        )
        with pytest.raises(Exception) as exc_info:
            self.module.get_headers()
        self.assertEqual(type(exc_info.value), Http404)

    def test_save_order_to_db(self):
        """Test save order to db method."""
        user = UserFactory()
        transaction_id = f'{random.randint(1, 1000)}'
        payment = self.module.save_order_to_db(
            number='Losowa-Liczba-123',
            price=0.01,
            email=self.tester_email,
            user=user,
            transaction_id=transaction_id,
        )
        self.assertEqual(payment.number, 'Losowa-Liczba-123')
        self.assertEqual(
            payment.price, Money(0.01, self.module.default_currency))
        self.assertEqual(payment.email, self.tester_email)
        self.assertEqual(payment.payer, user)
        self.assertEqual(payment.transaction_id, transaction_id)

    @override_settings(TPAY_RETURN_URL=None)
    def test_create_transaction_when_failure(self):
        """Test create transaction when there is failure."""
        user = UserFactory()
        result = self.module.create_transaction(
            user=user,
            amount=0.01,
            email=self.tester_email,
        )
        self.assertEqual(
            result,
            {'error': _('Return URL of TPay must be set in settings')},
        )

    @patch('requests.get')
    def test_get_transaction_simply(self, mock):
        """Test get transaction by simple way."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {'access_token': self.bearer_token},
        )
        result = self.module.get_transaction('123')
        self.assertEqual(result, {'access_token': self.bearer_token})

    @patch('requests.get')
    def test_get_transaction_with_exception(self, mock):
        """Test get transaction by raising empty data."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {'access_token': self.bearer_token},
        )
        result = self.module.get_transaction(self.nope_string_class())
        self.assertEqual(result, {})

    def test_get_all_transactions_with_broken_filters(self):
        """Test get all transactions with special filters."""
        result = self.module.get_all_transactions(
            limit='XYZ',
            from_dt='ABC',
            to_dt='CBA',
        )
        self.assertEqual(result, {})

    @patch('requests.get')
    @patch('requests.post')
    def test_get_all_transactions_with_filters(self, post, get):
        """Test get all transactions with special filters."""
        post.return_value = Mock(
            status_code=200,
            json=lambda: {'access_token': self.bearer_token},
        )
        get.return_value = Mock(
            status_code=200,
            json=lambda: {'data': 'example'},
        )
        result = self.module.get_all_transactions(
            limit='123',
            from_dt=datetime(year=2022, month=2, day=22),
            to_dt=datetime(year=2022, month=2, day=22),
        )
        self.assertEqual(result, {'data': 'example'})

    def test_get_url_address(self):
        """Test get url address method."""
        data = {
            'transactionPaymentUrl': 'https://google.pl',
        }
        result = self.module.get_url_address(data)
        self.assertEqual(result, 'https://google.pl')

    @override_settings(TPAY_MERCHANT_ID='1010')
    @patch('requests.get')
    def test_get_tpay_groups_different_than_200(self, mock):
        """Test get tpay groups when response is different than 200."""
        mock.return_value = Mock(
            status_code=201,
            json=lambda: {'access_token': self.bearer_token},
        )
        self.assertEqual(get_tpay_groups(), {})

    @override_settings(TPAY_MERCHANT_ID='1010')
    @patch('requests.get')
    def test_get_tpay_groups_simply(self, mock):
        """Test get tpay groups by simple way."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {'group': 123},
        )
        self.assertEqual(get_tpay_groups(), {'group': 123})

    @override_settings(TPAY_CLIENT_ID='1010')
    @override_settings(TPAY_CLIENT_SECRET='demo')
    @patch('requests.post')
    def test_pay_for_card_payment_simply(self, mock):
        """Test pay for card payment method by simple way."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {'access_token': self.bearer_token},
        )
        result = self.module.pay_for_card_payment(123, '123')
        self.assertEqual(result, {'access_token': self.bearer_token})

    @override_settings(TPAY_CLIENT_ID='1010')
    @override_settings(TPAY_CLIENT_SECRET='demo')
    @patch('requests.post')
    def test_pay_for_card_payment_with_exception(self, mock):
        """Test pay for card payment method by raising an exception."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {'access_token': self.bearer_token},
        )

        result = self.module.pay_for_card_payment(
            self.nope_string_class(), '123')
        self.assertEqual(result, {})

    @override_settings(TPAY_CLIENT_ID='1010')
    @override_settings(TPAY_CLIENT_SECRET='demo')
    @patch('requests.post')
    def test_pay_by_saved_card_payment_simply(self, mock):
        """Test pay for card payment method by simple way."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {'access_token': self.bearer_token},
        )
        result = self.module.pay_by_saved_card(123, '123')
        self.assertEqual(result, {'access_token': self.bearer_token})

    @override_settings(TPAY_CLIENT_ID='1010')
    @override_settings(TPAY_CLIENT_SECRET='demo')
    @patch('requests.post')
    def test_pay_by_saved_card_with_exception(self, mock):
        """Test pay for card payment method by raising an exception."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {'access_token': self.bearer_token},
        )

        result = self.module.pay_by_saved_card(
            self.nope_string_class(), '123')
        self.assertEqual(result, {})

    @override_settings(TPAY_MERCHANT_ID='1010')
    @patch('requests.get')
    def test_get_parsed_tpay_groups_failed(self, mock):
        """Test if get parded tpay groups has no json value."""
        mock.return_value = Mock(
            status_code=200,
            json=lambda: {},
        )
        self.assertEqual(get_parsed_tpay_groups(), [])

    @override_settings(TPAY_RETURN_URL='http://www.google.pl')
    @patch('tpay_module.tpay_api.TPayModule.get_headers')
    @patch('requests.post')
    def test_create_transaction_simple(self, post_mock, headers_mock):
        """Test create transaction by simple way."""
        response = {
            'result': 'success',
            'transactionId': 123,
            'testValue': 'testString',
        }
        post_mock.return_value = Mock(
            status_code=200,
            json=lambda: response,
        )
        headers_mock.return_value = {
            'Authorization': f'Bearer {self.bearer_token}',
        }
        user = UserFactory()
        test_response = self.module.create_transaction(
            user,
            0.01,
            self.tester_email,
            name='Patrick Szczepański',
            success_url='http://www.yahoo.pl',
            error_url='http://stackoverflow.com/',
        )
        self.assertEqual(response, test_response)
        get_payment = TPayPayment.objects.first()
        self.assertEqual(
            get_payment.transaction_id,
            '123',
        )
        self.assertEqual(
            get_payment.price,
            Money(0.01, self.module.default_currency),
        )
        self.assertEqual(get_payment.payer.id, user.id)

"""TPay OpenAPI integration."""

# Standard Libraries
import requests
import uuid

# Django
from django.conf import settings
from django.http import Http404
from django.utils.translation import gettext_lazy as _

# 3rd-party
from djmoney.money import Money


class TPayModule(object):
    """
    TPay module integration using new OpenAPI.
    Based on: https://openapi.tpay.com/
    """
    PAY_BY_LINK = 'pay_by_link'
    TRANSFER = 'transfer'
    CARD = 'sale'

    def __init__(self):
        """Init super method."""
        self.api_url = 'https://api.tpay.com'
        self.description = getattr(settings, 'TPAY_DESCRIPTION', 'Jakis opis')
        self.merchant_description = getattr(settings, 'TPAY_MERCHANT', 'Jakis dostawca')
        self.language = 'pl'
        self.country = 'PL'
        self.result_url = 'https://shop.tpay.com/shop-endpoint'
        self.return_url = 'https://shop.tpay.com/success'
        self.error_url = 'https://shop.tpay.com/error'
        self.default_currency = 'PLN'
        self.card_payment_id = 103  # groupId of card
        self.default_payment_id = 150  # groupId of default payment

    def get_headers(self):
        """Get headers for OAuth 2.0 auth using new TPay OpenAPI."""
        tpay_client_id = getattr(settings, 'TPAY_CLIENT_ID', None)
        tpay_client_secret = getattr(settings, 'TPAY_CLIENT_SECRET', None)
        if not tpay_client_id or not tpay_client_secret:
            raise Http404
        token_response = requests.post(f'{self.api_url}/oauth/auth', data={
            'client_id': tpay_client_id,
            'client_secret': tpay_client_secret,
        })
        if token_response.status_code == 200:
            access_token = token_response.json()['access_token']
            return {'Authorization': f'Bearer {access_token}'}
        raise Http404

    def save_order_to_db(self, number, price, email, transaction_id, user=None):
        """Save order to db."""
        pass
        # return TPayPayment.objects.create(
        #     number=number,
        #     price=Money(price, self.default_currency),
        #     email=email,
        #     user=user,
        #     transaction_id=transaction_id,
        # )

    def create_transaction(
        self,
        user,
        amount,
        email,
        name='',
        source='',
        method=PAY_BY_LINK,
        success_url=None,
        error_url=None,
        payment_group_id=None,
    ):
        """Return url that proceeds to created transaction."""
        if not getattr(settings, 'TPAY_RETURN_URL', None):
            return {
                'error': _('TPAY Return Url musi być ustawiony w settings.'),
            }
        payer_name = name
        if user and user is not None:
            payer_name = f'{user.first_name} {user.last_name}'
        payment_number = uuid.uuid4()
        payment_group_id = payment_group_id or self.default_payment_id
        data = {
            'amount': float(amount),
            'description': self.description,
            'hiddenDescription': f'{payment_number}',
            'lang': self.language,
            'payer': {
                'email': email,
                'name': payer_name,
            },
            'callbacks': {
                'notification': {
                    'url': f'{settings.TPAY_RETURN_URL}tpay-ipn/',
                },
            },
            'pay': {
                'groupId': payment_group_id,
            },
        }
        if payment_group_id != 103:
            data['pay']['method'] = method
        if success_url or error_url:
            data['callbacks']['payerUrls'] = {}
        if success_url:
            data['callbacks']['payerUrls']['success'] = success_url
        if error_url:
            data['callbacks']['payerUrls']['error'] = error_url
        if getattr(settings, 'TPAY_NOTIFY_EMAIL', None):
            data['callbacks']['notification']['email'] = settings.TPAY_NOTIFY_EMAIL
        try:
            response_data = requests.post(
                f'{self.api_url}/transactions',
                json=data, headers=self.get_headers(),
            ).json()
            if response_data.get('result', 'success') == 'success':
                self.save_order_to_db(
                    payment_number,
                    amount,
                    email,
                    response_data['transactionId'],
                    user,
                )
                return response_data
        except BaseException as e:  # noqa: D104
            pass
        return {}

    def pay_for_card_payment(self, transaction_id, card_data):
        data = {
            'groupId': self.card_payment_id,
            'cardPaymentData': {
                'card': card_data,
                'save': True,
            },
        }
        try:
            response_data = requests.post(
                f'{self.api_url}/transactions/{transaction_id}/pay',
                json=data, headers=self.get_headers(),
            ).json()
            return response_data
        except BaseException as e:
            pass
        return {}

    def pay_by_saved_card(self, transaction_id, card_token):
        data = {
            'groupId': self.card_payment_id,
            'cardPaymentData': {
                'token': card_token,
            },
            'method': 'sale',
        }
        try:
            response_data = requests.post(
                f'{self.api_url}/transactions/{transaction_id}/pay',
                json=data, headers=self.get_headers(),
            ).json()
            return response_data
        except BaseException as e:
            pass
        return {}

    def get_transaction(self, transaction_id):
        """Get certain transaction via transactionId field."""
        try:
            response_data = requests.get(
                f'{self.api_url}/transactions/{transaction_id}',
                json={}, headers=self.get_headers(),
            ).json()
            return response_data
        except BaseException as e:
            pass
        return {}

    def get_all_transactions(self, limit=None, from_dt=None, to_dt=None):
        """FOR NOW dummy method to get list of all transactions."""
        try:
            filter_data = {}
            if from_dt:
                filter_data['from'] = from_dt.strftime('%Y-%m-%d %H:%M:%S')
            if to_dt:
                filter_data['to'] = to_dt.strftime('%Y-%m-%d %H:%M:%S')
            if limit:
                filter_data['limit'] = int(limit)
            response_data = requests.get(
                f'{self.api_url}/transactions/',
                json=filter_data, headers=self.get_headers(),
            ).json()
            return response_data
        except BaseException as e:
            pass
        return {}

    def get_url_address(self, data):
        """
        Get url address that proceeds to payment from json data of response.
        """
        return data['transactionPaymentUrl']

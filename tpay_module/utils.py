"""TPay utils file."""
# Django
from django.conf import settings

# 3rd-party
import requests

# Project
from tpay_module.models import TPaySettings


def get_tpay_groups():
    """Get method of payments from tpay without data transform."""
    merchant_id = getattr(settings, 'TPAY_MERCHANT_ID', 1010)
    r = requests.get(f'https://secure.tpay.com/groups-{merchant_id}0.js?json')
    if r.status_code == 200:
        return r.json()
    return {}


def get_parsed_tpay_groups():
    """Get parsed TPay groups."""
    json = get_tpay_groups()
    if json:
        return [
            (item['id'], item['name'])
            for item in json.values()
        ]
    return []


def get_settings_from_db():
    """Get settings from db for TPay."""
    if getattr(settings, 'TPAY_ADMIN_SETTINGS', False):
        return TPaySettings.objects.first()

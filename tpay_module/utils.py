"""TPay utils file."""
# Django
from django.conf import settings

# 3rd-party
import requests

# Project
from tpay_module.consts import TPAY_SETTINGS_MODEL_MAPPING
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


def get_tpay_settings(specific_field=None):
    """Get tpay settings."""
    obj = None
    field_list = [
        'TPAY_RETURN_URL',
        'TPAY_CLIENT_ID',
        'TPAY_CLIENT_SECRET',
    ]
    if specific_field not in field_list:
        return None
    if getattr(settings, 'TPAY_ADMIN_SETTINGS', False):
        obj = TPaySettings.objects.first()
    mapping = TPAY_SETTINGS_MODEL_MAPPING if obj else {}
    result = {}
    for field in field_list:
        get_val = getattr(obj, mapping.get(field, None), None)
        settings_val = getattr(settings, field, None)
        if get_val:
            result[field] = get_val
        elif settings_val:
            result[field] = settings_val
    return result

import requests
from django.conf import settings


def get_tpay_groups():
    """
    Get method of payments from tpay without data transform.
    """
    merchant_id = getattr(settings, 'TPAY_MERCHANT_ID', 1010)
    r = requests.get(f'https://secure.tpay.com/groups-{merchant_id}0.js?json')
    if r.status_code == 200:
        return r.json()
    return {}


def get_parsed_tpay_groups():
    """
    Returns list of pairs: (group_id, group name) - methods of payments
    in TPAY.
    """
    json = get_tpay_groups()
    if json:
        return [
            (item['id'], item['name'])
            for item in json.values()
        ]
    return []
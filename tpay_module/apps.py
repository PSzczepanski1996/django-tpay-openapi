"""Apps file."""
# Django
from django.apps import AppConfig


class TpayModuleConfig(AppConfig):
    """Tpay module app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tpay_module'

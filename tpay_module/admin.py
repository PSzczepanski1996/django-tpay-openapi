"""TPay payment admin class."""
# Django
from django.conf import settings
from django.contrib import admin

# Project
from tpay_module.models import SavedTPayCard
from tpay_module.models import TPayPayment
from tpay_module.models import TPaySettings


@admin.register(TPayPayment)
class TPayPaymentAdmin(admin.ModelAdmin):
    """TPay Payment admin."""

    list_display = [
        'number',
        'email',
        'transaction_id',
        'created_dt',
    ]
    search_fields = [
        'number',
        'transaction_id',
        'email',
    ]


@admin.register(SavedTPayCard)
class SavedTPayCardAdmin(admin.ModelAdmin):
    """Saved TPay card."""

    search_fields = [
        'card_token',
    ]


class TPaySettingsAdmin(admin.ModelAdmin):
    """TPay Settings Admin."""

    pass


if getattr(settings, 'TPAY_ADMIN_SETTINGS', False):
    admin.site.register(TPaySettings)

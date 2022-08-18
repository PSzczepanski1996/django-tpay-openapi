"""TPay payment admin class."""

from django.contrib import admin


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


class SavedTPayCard(admin.ModelAdmin):
    """Saved TPay card."""

    search_fields = [
        'card_token',
    ]

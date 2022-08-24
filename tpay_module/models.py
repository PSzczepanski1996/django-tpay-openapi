"""Tpay Module."""
# Django
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# 3rd-party
from djmoney.models.fields import MoneyField

# Project
from tpay_module.mixins import SingleInstanceMixin

user_model = get_user_model()


class TPayPayment(models.Model):
    """Tpay Payment class."""

    # Payer is blank true null true for anonymous payments
    payer = models.ForeignKey(
        user_model,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name=_('Email'),
    )
    number = models.CharField(
        _('UUID Payment number'),
        max_length=255, unique=True,
        db_index=True,
    )
    price = MoneyField(
        _('Price'),
        max_digits=14,
        decimal_places=2,
        default_currency='PLN',
    )
    transaction_id = models.CharField(
        _('Transaction ID'),
        max_length=255,
    )
    created_dt = models.DateTimeField(
        _('Created at'), auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        _('Modified at'), auto_now=True,
    )

    def __str__(self):  # noqa: D105
        return _('Transaction {0}').format(self.number)

    class Meta:  # noqa: D106
        verbose_name = _('TPay Payment')
        verbose_name_plural = _('TPay Payments')
        ordering = ['-created_dt']


class SavedTPayCard(models.Model):
    """Saved Tpay card."""

    card_token = models.CharField(_('Card token'), max_length=255)
    card_expiration_code = models.CharField(
        _('Card expiration code'),
        max_length=4,
        default='0000',
    )
    created_dt = models.DateTimeField(
        _('Created at'), auto_now_add=True)
    last_used = models.DateTimeField(
        _('Last used'),
        null=True, blank=True,
    )

    def __str__(self):  # noqa: D105
        return _('Saved TPay Card ({0})').format(self.id)

    class Meta:  # noqa: D106
        verbose_name = _('Saved TPay Card')
        verbose_name_plural = _('Saved TPay Cards.')


class TPaySettings(SingleInstanceMixin, models.Model):
    """Custom TPay Settings - for admin user."""

    return_url = models.CharField(
        _('Return URL (IPN)'),
        max_length=255,
        blank=True,
        null=True,
    )
    client_id = models.CharField(
        _('Client ID'),
        max_length=255,
        blank=True,
        null=True,
    )
    client_secret = models.CharField(
        _('Client secret'),
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):  # noqa: D105
        return _('TPay Settings')

    class Meta:  # noqa: D106
        verbose_name = _('TPay Settings')
        verbose_name_plural = _('TPay Settings')

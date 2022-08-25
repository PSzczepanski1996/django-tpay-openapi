"""Forms file."""
# Django
from django import forms
from django.utils.translation import gettext_lazy as _

# Project
from tpay_module.models import TPayPayment


class TPayIPNForm(forms.Form):
    """TPay IPN response form."""

    FAILURE_STATUS = 'FALSE'
    SUCCESS_STATUS = 'TRUE'
    status_choices = (
        (FAILURE_STATUS, _('Failure')),
        (SUCCESS_STATUS, _('Success')),
    )
    TEST_MODE = (
        (0, 'Disabled'),
        (1, 'Enabled'),
    )

    id = forms.CharField(
        max_length=64,
    )
    tr_id = forms.CharField(
        max_length=64,
    )
    tr_date = forms.DateTimeField(required=False)
    tr_crc = forms.ModelChoiceField(
        queryset=TPayPayment.objects.all(),
        to_field_name='number',
    )
    tr_paid = forms.DecimalField()
    tr_status = forms.ChoiceField(
        choices=status_choices)
    tr_email = forms.EmailField(
        required=False)
    md5sum = forms.CharField(
        max_length=32,
        required=False,
    )

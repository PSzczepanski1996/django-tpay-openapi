"""Forms file."""
# Django
from django import forms

# Project
from tpay_module.models import TPayPayment


class TPayIPNForm(forms.Form):
    """TPay IPN response form."""

    FAILURE_STATUS = 'FALSE'
    SUCCESS_STATUS = 'TRUE'
    status_choices = (
        (FAILURE_STATUS, 'Failure'),
        (SUCCESS_STATUS, 'Success'),
    )

    tr_id = forms.CharField(
        max_length=64,
    )
    tr_date = forms.DateTimeField(required=False)
    tr_crc = forms.ChoiceField()
    tr_paid = forms.DecimalField()
    tr_status = forms.ChoiceField(
        choices=status_choices)
    tr_email = forms.EmailField(
        required=False)

    def __init__(self, *args, **kwargs):  # noqa: D107
        super().__init__(*args, **kwargs)
        payment_choices = [
            (value, value) for value in
            TPayPayment.objects.values_list('number', flat=True)
        ]
        self.fields['tr_crc'].choices = payment_choices

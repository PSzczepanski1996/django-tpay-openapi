"""Template tags for TPay library."""
# Django
from django import template

# Project
from tpay_module.models import TPayPayment

register = template.Library()


@register.simple_tag()
def get_tpay_payment(transaction_id):
    """Get TPay payment based on transaction ID."""
    return TPayPayment.objects.filter(
        transaction_id=transaction_id).first()

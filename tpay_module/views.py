"""TPay IPN viewset."""
# Standard Library
import hashlib
from decimal import Decimal

# Django
from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.views import View

# Project
from tpay_module.models import TPayPayment


class TPayIpnHandler(View):
    """Tpay Ipn Handler class."""

    model = TPayPayment
    success_respose = 'TRUE'
    failure_response = 'FALSE'

    def get(self, request, *args, **kwargs):
        """Disable get handler entirely."""
        raise Http404

    def custom_callback(self, payment, failure=False):
        """Execute custom callback."""
        pass

    def dispatch(self, request, *args, **kwargs):  # noqa: D102
        if getattr(settings, 'TPAY_DISABLE', False):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # noqa: D102
        data = request.POST
        payment_number = data['tr_crc']
        try:
            payment = self.model.objects.get(number=payment_number)
            payment_part = f'{payment.price.amount}{payment.number}'
            secure_code = getattr(settings, 'TPAY_SECURE_CODE', None)
            if secure_code:
                probable_md5 = hashlib.md5(
                    f'{data["id"]}{data["tr_id"]}{payment_part}{secure_code}'.encode('utf-8'),
                ).hexdigest()
                get_price = '{:.2f}'.format(float(request.POST['tr_paid']))  # noqa: P101
                price_check = Decimal(get_price) == payment.price.amount
                md5_check = request.POST['md5sum'] == probable_md5
                if price_check and md5_check and not payment.is_finished:
                    payment.is_finished = True
                    payment.save()
                    self.custom_callback(payment)
                    return HttpResponse('TRUE')
        except TPayPayment.DoesNotExist:
            pass
        self.custom_callback(None, True)
        return HttpResponse(self.success_respose)

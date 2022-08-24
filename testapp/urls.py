"""TestAPP url config."""
# Django
from django.contrib import admin
from django.urls import path

# Project
from tpay_module.views import TPayIpnHandler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tpay-ipn/', TPayIpnHandler.as_view(), name='tpay_ipn'),
]

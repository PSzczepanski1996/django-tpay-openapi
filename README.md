# django-tpay-openapi

This is Tpay polish payment broker library, it should avoid few (many?) headaches while implementing it with OpenAPI backend, which is quite new.

The current version is highly experimental (and it's just python class module) - in future it should contain enough login to plug-in it as Django application in `INSTALLED_APPS`.

### Features:
* Based on code from working, quite popular project (with over 1k active clients).
* Just SINGLE dependency (not even Django is required for now, but `requests` library is a must).
* Written in extensible way

### Settings:
`TPAY_MERCHANT_ID` - as it says... it's tpay merchant id.
to be c.d.n.

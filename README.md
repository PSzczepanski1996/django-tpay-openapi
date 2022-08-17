# django-tpay-openapi

This is Tpay polish payment broker library, it should avoid few (many?) headaches while implementing it with OpenAPI backend, which is quite new.

The current version is highly experimental (and it's just python class module) - in future it should contain enough login to plug-in it as Django application in `INSTALLED_APPS`.

### Features:
* Based on code from working, quite popular project (tested with multiple customers).
* Just SINGLE dependency (not even Django is required for now, but `requests` library is a must).
* Probably in future it will depend on Django Money for multicurrency handling.
* Written in extensible way!

### Settings:
`TPAY_CLIENT_ID` - client ID from tpay settings.
`TPAY_CLIENT_SECRET` - secret from tpay settings.
`TPAY_RETURN_URL` - TPAY IPN settings, MUST BE SET to django endpoint (can be tested with ngrok).
`TPAY_MERCHANT_ID` - as it says... it's tpay merchant id.
`TPAY_DESCRIPTION` - TPay payment description.
`TPAY_MERCHANT` - TPay merchant description.

### Can I get your help?
Sure, but don't expect I will respond in quite short amount of time. The class can't be plugged by simple way into Django code now,
instead you need to rewrite small amount of code in it to get it working in your own project.
Anyway I think it can give you insight how tpay openapi works and avoid you eternal pain from emptiness and sadness while trying to debug "why it's not working".

### to be c.d.n.
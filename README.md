![django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![json](https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white)

# django-tpay-openapi

This is payment broker library for TPay services, it should avoid few (many?) headaches while implementing it with OpenAPI backend, which is quite new.

The current version is highly experimental (and it's just python class module) ~~- in future it should contain enough login to plug-in it as Django application in `INSTALLED_APPS`.~~

### Features:
* Django plug-in support that provides additional methods and models
* Based on *my own* code from working, quite popular project (tested with multiple customers)
* Multicurrency handling is almost implemented
* Written in highly abstract and extensible way
* Is much more clean and has better performance than OpenAPI automatically generated code
* TPay notification-system (IPN) support
* Is translated in english language besides polish

### Installation process:
Add the TPay app to the `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'tpay_module.apps.TpayModuleConfig',
    ...
]
```

Plug-in TPay notification handler (IPN) for updating statuses into project urls:
```python
path('tpay-ipn/', TPayIpnHandler.as_view(), name='tpay_ipn'),
```

Then, write code that will handle payments using TPayModule class.  
The examples will be providen soon (how to create transaction and et cetera).

### Django available custom settings:
`TPAY_CLIENT_ID` - client ID from tpay settings.  
`TPAY_CLIENT_SECRET` - secret from tpay settings.  
`TPAY_RETURN_URL` - TPAY IPN settings, MUST BE SET to django endpoint (can be tested with ngrok).  
`TPAY_MERCHANT_ID` - as it says... it's tpay merchant id.  
`TPAY_DESCRIPTION` - TPay payment description.  
`TPAY_MERCHANT` - TPay merchant description.  

### I need to provide custom admin model for my client, can I do that?
Sure! The library is made with expandability in mind, so it contains custom admin settings model.
The model instance is able to override settings from Django if it's necessary using custom handler logic.

The model in admin is initially disabled, you need to set `TPAY_ADMIN_SETTINGS` to `True` val.

### Can I get your help?
Sure, but don't expect I will respond in quite short amount of time. The class can't be plugged by simple way into Django code now,
instead you need to rewrite small amount of code in it to get it working in your own project.
Anyway I think it can give you insight how tpay openapi works and avoid you eternal pain from emptiness and sadness while trying to debug "why it's not working".

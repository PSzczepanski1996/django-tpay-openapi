"""Test misc stuff."""
# Django
from django.core.handlers.asgi import ASGIHandler
from django.core.handlers.wsgi import WSGIHandler
from django.test import TestCase


class MiscTests(TestCase):
    """Misc tests."""

    def setUp(self):
        """Set method.."""
        pass

    def test_wsgi_app(self):
        """Test wsgi application."""
        # Local
        from ..wsgi import application
        wsgi_app = application
        self.assertEqual(type(wsgi_app), WSGIHandler)

    def test_asgi_app(self):
        """Test wsgi application."""
        # Local
        from ..asgi import application
        asgi_app = application
        self.assertEqual(type(asgi_app), ASGIHandler)

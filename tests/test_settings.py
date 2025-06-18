# tests/test_settings.py
from django.test import TestCase
from django.conf import settings

class SettingsTests(TestCase):
    def test_installed_apps(self):
        self.assertIn('peliculas', settings.INSTALLED_APPS)
        self.assertIn('rest_framework', settings.INSTALLED_APPS)

    def test_debug_mode(self):
        self.assertFalse(settings.DEBUG)  # Debe ser False en producción
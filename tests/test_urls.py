# tests/test_urls.py
from django.test import TestCase
from django.urls import reverse, resolve

class UrlsTests(TestCase):
    def test_api_urls(self):
        path = '/api/peliculas/'
        self.assertEqual(resolve(path).view_name, 'peliculas-list')
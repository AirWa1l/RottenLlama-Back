# conftest.py
import os
import django

def pytest_configure():
    # Ajusta aquí el path a tu settings.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RottenLlama.settings')
    django.setup()

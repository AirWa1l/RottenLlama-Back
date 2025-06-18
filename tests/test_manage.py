# tests/test_manage.py
from django.core.management import call_command
from io import StringIO
import pytest

def test_check_command():
    out = StringIO()
    call_command('check', stdout=out)
    assert 'System check identified no issues' in out.getvalue()

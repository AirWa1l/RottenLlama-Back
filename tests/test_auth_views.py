# tests/test_auth_views.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def valid_user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123!"
    }

@pytest.mark.django_db
class TestRegisterView:
    def test_register_valid_user(self, api_client, valid_user_data):
        url = '/api/auth/register/'
        response = api_client.post(url, valid_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=valid_user_data['email']).exists()
        assert 'user' in response.data
        assert 'access' in response.data
        assert 'refresh' in response.data
        
        user = User.objects.get(email=valid_user_data['email'])
        assert user.check_password(valid_user_data['password'])

    def test_register_duplicate_email(self, api_client, valid_user_data):
        # Primero creamos un usuario
        api_client.post('/api/auth/register/', valid_user_data)
        
        # Intentamos crear otro con el mismo email
        response = api_client.post('/api/auth/register/', valid_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_missing_fields(self, api_client):
        invalid_data = [
            {"email": "", "username": "test", "password": "Test123!"},
            {"email": "test@example.com", "username": "", "password": "Test123!"},
            {"email": "test@example.com", "username": "test", "password": ""},
        ]
        
        for data in invalid_data:
            response = api_client.post('/api/auth/register/', data)
            assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestLoginView:
    def test_login_valid_credentials(self, api_client):
        # Primero crea un usuario
        CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="TestPass123!"
        )
        
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {
            "email": "test@example.com",
            "password": "TestPass123!"
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

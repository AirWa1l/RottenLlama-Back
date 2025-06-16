import pytest
from django.urls import reverse
from users.models import CustomUser
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123"
    }

@pytest.fixture
def register_url():
    return reverse('register')

@pytest.fixture
def login_url():
    return reverse('token_obtain_pair')

@pytest.fixture
def refresh_url():
    return reverse('token_refresh')

@pytest.mark.django_db
def test_user_registration(api_client, user_data, register_url):
    response = api_client.post(register_url, user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert CustomUser.objects.filter(email=user_data["email"]).exists()

@pytest.mark.django_db
def test_login_with_valid_credentials(api_client, user_data, register_url, login_url):
    api_client.post(register_url, user_data)
    response = api_client.post(login_url, {
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_login_with_invalid_credentials(api_client, login_url):
    response = api_client.post(login_url, {
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_refresh_token(api_client, user_data, register_url, login_url, refresh_url):
    api_client.post(register_url, user_data)
    login_response = api_client.post(login_url, {
        "email": user_data["email"],
        "password": user_data["password"]
    })
    refresh = login_response.data["refresh"]
    response = api_client.post(refresh_url, {"refresh": refresh})
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data

@pytest.mark.django_db
def test_register_duplicate_email(api_client, user_data, register_url):
    api_client.post(register_url, user_data)
    response = api_client.post(register_url, user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data

@pytest.mark.django_db
def test_register_missing_fields(api_client, register_url):
    response = api_client.post(register_url, {
        "email": "",
        "username": "",
        "password": ""
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
    assert "username" in response.data
    assert "password" in response.data

@pytest.mark.django_db
def test_register_does_not_return_password(api_client, user_data, register_url):
    response = api_client.post(register_url, user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "password" not in response.data

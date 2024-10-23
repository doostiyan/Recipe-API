import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def create_user():
    return User.objects.create_user(email="test@example.com", password="passwordtest", name="test name")


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def authenticated_client(client, create_user):
    auth = client.force_authenticate(create_user)
    return auth

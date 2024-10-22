import pytest
from users.models import User


@pytest.fixture
def create_user():
    return User.objects.create_user(email="test@example.com", password="passwordtest", name="test name")

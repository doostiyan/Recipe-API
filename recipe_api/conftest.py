from decimal import Decimal

import pytest
from recipes.models import Recipe
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
    client.force_authenticate(create_user)
    return client


@pytest.fixture
def create_admin_user(client):
    admin = User.objects.create_superuser(email="admin@example.com", password="passwordtest")
    client.force_login(admin)
    return admin


@pytest.fixture
def create_user_param():
    def make_user(**params):
        return User.objects.create_user(**params)

    return make_user


@pytest.fixture
def create_recipe(create_user):
    def _create_recipe(user, **params):
        default = {
            "title": "Simple recipe title",
            "time_minutes": 10,
            "price": Decimal(5.25),
            "description": "Simple description",
            "link": "http://example.com/recipe.pdf",
        }
        default.update(params)
        return Recipe.objects.create(user=user, **default)

    return _create_recipe

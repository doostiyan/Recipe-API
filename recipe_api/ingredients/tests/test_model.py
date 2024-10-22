import pytest

from ingredients.models import Ingredient


@pytest.mark.django_db
def test_create_ingredient(create_user):
    user = create_user
    ingredient = Ingredient.objects.create(user=user, name="Salt")

    assert ingredient.name == "Salt"

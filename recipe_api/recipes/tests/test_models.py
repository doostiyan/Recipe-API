import os
from decimal import Decimal
from unittest.mock import patch

import pytest

from recipes import models
from recipes.models import Recipe


@pytest.mark.django_db
class TestRecipe:
    def test_create_recipe(self, create_user):
        recipe = Recipe.objects.create(
            user=create_user,
            title="test title",
            time_minutes=10,
            price=Decimal("5.5"),
            description="test description",
        )
        assert str(recipe) == recipe.title


@pytest.mark.django_db
@patch("uuid.uuid4")
def test_recipe_file_name_uuid(mock_uuid):
    """Test generating image path."""
    uuid = "test-uuid"
    mock_uuid.return_value = uuid
    file_path = models.recipe_image_file_path(None, "example.jpg")

    expected_path = os.path.join("uploads", "recipe", f"{uuid}.jpg")
    assert file_path == expected_path

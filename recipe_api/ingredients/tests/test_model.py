from unittest.mock import patch

from django.test import TestCase
from users.models import User

from ingredients import models


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return User.objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_ingredient(self):
        user = create_user()
        ingredient = models.Ingredient.objects.create(user=user, name="Ingredient1")

        self.assertEqual(str(ingredient), ingredient.name)

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")

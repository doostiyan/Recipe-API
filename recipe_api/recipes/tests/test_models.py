from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from recipes import models
from recipes.models import Recipe
from users.models import User


class TestRecipe(TestCase):
    def test_create_recipe(self):
        user = User.objects.create_user(
            email = 'test@example.com',
            password= 'passwordtest',
            name = 'test name '
        )
        recipe = Recipe.objects.create(
            user = user,
            title = 'test title',
            time_minutes = 10,
            price = Decimal('5.5'),
            description = 'test description',
        )
        self.assertEqual(str(recipe), recipe.title)


    @patch('recipes.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
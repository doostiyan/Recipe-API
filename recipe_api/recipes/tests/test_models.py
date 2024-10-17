from decimal import Decimal

from django.test import TestCase

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

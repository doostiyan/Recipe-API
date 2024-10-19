from django.test import TestCase

from ingredients import models
from users.models import User


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return User.objects.create_user(email, password)

class ModelTests(TestCase):
    def test_create_ingredient(self):
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

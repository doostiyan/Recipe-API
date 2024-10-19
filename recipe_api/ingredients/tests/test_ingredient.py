from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer
from users.models import User

INGREDIENT_URL = reverse('ingredient:ingredient-list')

def detail_url(ingredient_id):
    return reverse('ingredient:ingredient-detail', args=[ingredient_id])

def create_user(email='user@example.com', password='passwordtest'):
    return User.objects.create_user(email=email, password=password)

class PublicIngredientApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)
    def test_retrieve_ingredient(self):
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.craete(user=self.user, name='Vanilla')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        user2 = create_user(email='user@example.com')
        Ingredient.objects.create(user=user2, name='Salt')
        ingredient = Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name='Cilantro')

        payload = {'name': 'Coriander'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name='Lettuce')
        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredient.refresh_from_db()
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertEqual(ingredients.exists())

    def test_filter_ingredient_assigned_to_recipe(self):
        pass
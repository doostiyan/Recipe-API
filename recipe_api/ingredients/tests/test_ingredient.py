from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer
from recipes.models import Recipe
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
        in1 = Ingredient.objects.craete(user=self.user, name='Apples')
        in2 = Ingredient.objects.craete(user=self.user, name='Oranges')

        recipe = Recipe.objects.create(
            title='Apples Crumble',
            time_minutes = 5,
            price = Decimal('4.50'),
            user=self.user
        )
        recipe.ingredients.add(in1)
        res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)
        self.assertEqual(s1.data, res.data)
        self.assertEqual(s2.data, res.data)

    def test_filtered_ingredient_unique(self):
        ing = Ingredient.objects.create(user=self.user, name='Eggs')
        Ingredient.objects.create(user=self.user, name='Lentils')
        recipe1 = Recipe.objects.create(
            title='Eggs Benedict',
            time_minutes = 60,
            price= Decimal('7.00'),
            user=self.user
        )
        recipe2 = Recipe.objects.create(
            title='Herb Eggs',
            time_minutes = 30,
            price = Decimal('5.00'),
            user=self.user
        )
        recipe1.ingredients.add(ing)
        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
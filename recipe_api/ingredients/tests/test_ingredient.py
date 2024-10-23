from decimal import Decimal

import pytest
from django.urls import reverse
from recipes.models import Recipe
from rest_framework import status
from users.models import User

from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer

INGREDIENT_URL = reverse("ingredients:ingredient-list")


def detail_url(ingredient_id):
    return reverse("ingredients:ingredient-detail", args=[ingredient_id])


@pytest.mark.django_db
class TestPublicIngredientApi:
    def test_auth_required(self, client):
        res = client.get(INGREDIENT_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateIngredientApi:
    def test_retrieve_ingredient(self, client, create_user, authenticated_client):
        Ingredient.objects.create(user=create_user, name="Kale")
        Ingredient.objects.create(user=create_user, name="Vanilla")

        res = client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        assert res.status_code == status.HTTP_200_OK
        assert res.data[0]["name"] == "Vanilla"
        assert res.data[1]["name"] == "Kale"
        assert sorted(res.data, key=lambda x: x["id"]) == sorted(serializer.data, key=lambda x: x["id"])

    def test_ingredient_limited_to_user(self, client, create_user, authenticated_client):
        user2 = User.objects.create_user(email="user2@examplee", password="passwordtest")
        Ingredient.objects.create(user=user2, name="Salt")
        ingredient = Ingredient.objects.create(user=create_user, name="Pepper")

        res = client.get(INGREDIENT_URL)

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        assert res.data[0]["name"] == ingredient.name
        assert res.data[0]["id"] == ingredient.id

    def test_update_ingredient(self, client, create_user, authenticated_client):
        ingredient = Ingredient.objects.create(user=create_user, name="Cilantro")

        payload = {"name": "Salt"}
        url = detail_url(ingredient.id)
        res = client.patch(url, payload)

        assert res.status_code == status.HTTP_200_OK
        ingredient.refresh_from_db()
        assert ingredient.name == payload["name"]

    def test_update_ingredient_not_owned(self, client, authenticated_client):
        other_user = User.objects.create_user(email="user2@examplee", password="passwordtest")
        ingredient = Ingredient.objects.create(user=other_user, name="Coriander")

        payload = {"name": "Salt"}
        url = detail_url(ingredient.id)
        res = client.patch(url, payload)
        assert res.status_code == status.HTTP_404_NOT_FOUND
        ingredient.refresh_from_db()
        assert ingredient.name == "Coriander"

    def test_delete_ingredient(self, client, create_user, authenticated_client):
        ingredient = Ingredient.objects.create(user=create_user, name="Lettuce")
        url = detail_url(ingredient.id)
        res = client.delete(url)

        assert res.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(Ingredient.DoesNotExist):
            ingredient.refresh_from_db()

    def test_delete_ingredient_not_owned(self, client, authenticated_client):
        other_user = User.objects.create_user(email="user2@examplee", password="passwordtest")
        ingredient = Ingredient.objects.create(user=other_user, name="Coriander")

        url = detail_url(ingredient.id)
        res = client.delete(url)

        assert res.status_code == status.HTTP_404_NOT_FOUND
        ingredient.refresh_from_db()
        assert ingredient is not None

    def test_filter_ingredient_assigned_to_recipe(self, client, create_user, authenticated_client):
        in1 = Ingredient.objects.create(user=create_user, name="Apples")
        in2 = Ingredient.objects.create(user=create_user, name="Oranges")

        recipe = Recipe.objects.create(title="Apples Crumble", time_minutes=5, price=Decimal("4.50"), user=create_user)
        recipe.ingredients.add(in1)
        res = client.get(INGREDIENT_URL, {"assigned_only": 1})

        s1 = IngredientSerializer(in1)
        assert s1.data in res.data
        assert IngredientSerializer(in2).data not in res.data

    def test_filtered_ingredient_unique(self, client, create_user, authenticated_client):
        ing = Ingredient.objects.create(user=create_user, name="Eggs")
        Ingredient.objects.create(user=create_user, name="Lentils")
        recipe1 = Recipe.objects.create(title="Eggs Benedict", time_minutes=60, price=Decimal("7.00"), user=create_user)
        recipe2 = Recipe.objects.create(title="Herb Eggs", time_minutes=30, price=Decimal("5.00"), user=create_user)
        recipe1.ingredients.add(ing)
        recipe2.ingredients.add(ing)

        res = client.get(INGREDIENT_URL, {"assigned_only": 1})
        assert len(res.data) == 1
        assert res.data[0]["name"] == "Eggs"
        rec = Ingredient.objects.get(name="Eggs").recipe_set.all()
        assert rec.count() == 2

import os
import tempfile
from decimal import Decimal

import pytest
from django.urls import reverse
from ingredients.models import Ingredient
from PIL import Image
from rest_framework import status
from tags.models import Tag
from users.models import User

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from recipes.serializers.recipe import RecipeDetailSerializer

RECIPES_URL = reverse("recipes:recipe-list")


def detail_url(recipe_id):
    return reverse("recipes:recipe-detail", args=[recipe_id])


def image_upload_url(recipe_id):
    return reverse("recipes:recipe-upload-image", args=[recipe_id])


@pytest.mark.django_db
class TestPublicRecipeApi:
    def test_auth_required(self, client):
        res = client.get(RECIPES_URL)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateRecipeApi:
    def test_retrieve_recipes(self, client, create_user, create_recipe):
        client.force_authenticate(user=create_user)
        create_recipe(user=create_user)
        create_recipe(user=create_user)

        assert Recipe.objects.count() == 2
        res = client.get(RECIPES_URL)

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 2
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        assert res.data == serializer.data

    def test_recipe_list_limited_to_user(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        other_user = User.objects.create_user(email="other@example.com", password="passwordtest")
        create_recipe(user=other_user)
        create_recipe(user=create_user)

        res = client.get(RECIPES_URL)
        recipe = Recipe.objects.filter(user=create_user)
        serializer = RecipeSerializer(recipe, many=True)
        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_get_recipe_detail(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        recipe = create_recipe(user=create_user)
        url = detail_url(recipe.id)
        res = client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        assert res.data == serializer.data

    def test_create_recipe(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        payload = {"title": "Simple recipe", "time_minutes": 30, "price": Decimal("5.99")}
        res = client.post(RECIPES_URL, payload)

        assert res.status_code == status.HTTP_201_CREATED
        recipe = Recipe.objects.get(id=res.data["id"])
        for k, v in payload.items():
            assert getattr(recipe, k) == v

        assert recipe.user == create_user

    def test_update_recipe(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        original_link = "https://example.com/recipe.pdf"
        recipe = create_recipe(user=create_user, title="Simple recipe title", link=original_link)
        payload = {"title": "New recipe title"}
        url = detail_url(recipe.id)
        res = client.patch(url, payload)

        assert res.status_code == status.HTTP_200_OK
        recipe.refresh_from_db()
        assert recipe.title == payload["title"]
        assert recipe.link == original_link
        assert recipe.user == create_user

    def test_full_update_recipe(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        recipe = create_recipe(
            user=create_user,
            title="Simple recipe title",
            link="http://example.com/recipe.pdf",
            description="Simple description",
            time_minutes=40,
            price=Decimal("9.99"),
        )
        payload = {
            "title": "New recipe title",
            "link": "https://example.com/recipe.pdf",
            "description": "New recipe  description",
            "time_minutes": 30,
            "price": Decimal("5.99"),
        }
        url = detail_url(recipe.id)
        res = client.patch(url, payload)
        assert res.status_code == status.HTTP_200_OK
        recipe.refresh_from_db()
        for k, v in payload.items():
            assert getattr(recipe, k) == v
        assert recipe.user == create_user

    def test_delete_recipe(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        recipe = create_recipe(user=create_user)
        url = detail_url(recipe.id)
        res = client.delete(url)

        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert not Recipe.objects.filter(id=recipe.id).exists()

    def test_delete_other_user_recipe_error(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        new_user = User.objects.create_user(email="user2@example.com", password="passwordtest")
        recipe = create_recipe(user=new_user)

        url = detail_url(recipe.id)
        res = client.delete(url)

        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert Recipe.objects.filter(id=recipe.id).exists()

    def test_create_recipe_with_new_tags(self, client, create_user):
        client.force_authenticate(create_user)
        payload = {
            "title": "Thai Prawn Curry",
            "time_minutes": 30,
            "price": Decimal("5.99"),
            "tags": [{"name": "Thai"}, {"name": "Dinner"}],
        }
        res = client.post(RECIPES_URL, payload, format="json")

        assert res.status_code == status.HTTP_201_CREATED
        recipes = Recipe.objects.filter(user=create_user)
        assert recipes.count() == 1
        recipe = recipes[0]
        assert recipe.tags.count() == 2
        for tag in payload["tags"]:
            exists = recipe.tags.filter(name=tag["name"], user=create_user).exists()
            assert exists

    def test_create_recipe_with_existing_tags(self, client, create_user):
        client.force_authenticate(create_user)
        tag_indian = Tag.objects.create(user=create_user, name="Indian")
        payload = {
            "title": "Pongal",
            "time_minutes": 30,
            "price": Decimal("5.99"),
            "tags": [{"name": "Indian"}, {"name": "Breakfast"}],
        }
        res = client.post(RECIPES_URL, payload, format="json")

        assert res.status_code == status.HTTP_201_CREATED
        recipes = Recipe.objects.filter(user=create_user)
        assert recipes.count() == 1
        recipe = recipes[0]
        assert recipe.tags.count() == 2
        assert tag_indian in recipe.tags.all()
        for tag in payload["tags"]:
            exists = recipe.tags.filter(name=tag["name"], user=create_user).exists()
            assert exists

    def test_create_tag_on_update(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        recipe = create_recipe(user=create_user)
        payload = {"tags": [{"name": "Lunch"}]}
        url = detail_url(recipe.id)
        res = client.patch(url, payload, format="json")

        assert res.status_code == status.HTTP_200_OK
        new_tag = Tag.objects.get(user=create_user, name="Lunch")
        assert new_tag in recipe.tags.all()

    def test_update_recipe_assign_tag(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        tag_breakfast = Tag.objects.create(user=create_user, name="Breakfast")
        recipe = create_recipe(user=create_user)
        recipe.tags.add(tag_breakfast)

        tag_lunch = Tag.objects.create(user=create_user, name="Lunch")
        payload = {"tags": [{"name": "Lunch"}]}
        url = detail_url(recipe.id)
        res = client.patch(url, payload, format="json")

        assert res.status_code == status.HTTP_200_OK
        assert tag_lunch in recipe.tags.all()
        assert tag_breakfast not in recipe.tags.all()

    def test_create_recipe_with_new_ingredients(self, client, create_user):
        client.force_authenticate(create_user)
        payload = {
            "title": "Cauliflower Tacos",
            "time_minutes": 30,
            "price": Decimal("4.30"),
            "ingredients": [{"name": "cauliflower"}, {"name": "salt"}],
        }
        res = client.post(RECIPES_URL, payload, format="json")

        assert res.status_code == status.HTTP_201_CREATED
        recipes = Recipe.objects.filter(user=create_user)
        assert recipes.count() == 1
        recipe = recipes[0]
        assert recipe.ingredients.count() == 2
        for ingredient in payload["ingredients"]:
            exists = recipe.ingredients.filter(name=ingredient["name"], user=create_user).exists()
            assert exists

    def test_create_recipe_with_existing_ingredients(self, client, create_user, create_recipe):
        client.force_authenticate(create_user)
        ingredient = Ingredient.objects.create(user=create_user, name="Lemon")
        payload = {
            "title": "Vietnamese Soup",
            "time_minutes": 25,
            "price": "2.55",
            "ingredients": [{"name": "Lemon"}, {"name": "Fish Sauce"}],
        }
        res = client.post(RECIPES_URL, payload, format="json")
        assert res.status_code == status.HTTP_201_CREATED
        recipes = Recipe.objects.filter(user=create_user)
        assert recipes.count() == 1
        recipe = recipes[0]
        assert recipe.ingredients.count() == 2
        assert ingredient in recipe.ingredients.all()
        for ingredient in payload["ingredients"]:
            exists = recipe.ingredients.filter(name=ingredient["name"], user=create_user).exists()
            assert exists


@pytest.mark.django_db
class TestImageUpload:
    def test_upload_image(self, client, create_user):
        client.force_authenticate(create_user)
        recipe = Recipe.objects.create(
            user=create_user,
            title="Sample recipe",
            time_minutes=10,
            price=Decimal("5.25"),
            description="This is a sample recipe",
            link="http://example.com",
        )
        url = image_upload_url(recipe.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"image": image_file}
            res = client.post(url, payload, format="multipart")

        recipe.refresh_from_db()
        assert res.status_code == status.HTTP_200_OK
        assert "image" in res.data
        assert os.path.exists(recipe.image.path)

    def test_upload_image_bad_request(self, client, create_user):
        client.force_authenticate(create_user)
        recipe = Recipe.objects.create(
            user=create_user,
            title="Sample recipe",
            time_minutes=10,
            price=Decimal("5.25"),
        )

        url = image_upload_url(recipe.id)
        payload = {"image": "notanimage"}
        res = client.post(url, payload, format="multipart")

        assert res.status_code == status.HTTP_400_BAD_REQUEST

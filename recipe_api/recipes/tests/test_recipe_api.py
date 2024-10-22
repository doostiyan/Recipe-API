# import os
# import tempfile
# from decimal import Decimal
#
# from django.test import TestCase
# from django.urls import reverse
# from ingredients.models import Ingredient
# from PIL import Image
# from rest_framework import status
# from rest_framework.test import APIClient
# from tags.models import Tag
# from users.models import User
#
# from recipes.models import Recipe
# from recipes.serializers import RecipeSerializer
#
# RECIPES_URL = reverse("recipes:recipe-list")
#
#
# def detail_url(recipe_id):
#     return reverse("recipes:recipe-detail", args=recipe_id)
#
#
# def image_upload_url(recipe_id):
#     return reverse("recipes:recipe-upload_image", args=[recipe_id])
#
#
# def create_recipe(user, **params):
#     default = {
#         "title": "Simple recipe title",
#         "time_minutes": 10,
#         "price": Decimal(5.25),
#         "description": "Simple description",
#         "link": "http://example.com/recipe.pdf",
#     }
#     default.update(params)
#     recipe = Recipe.objects.create(user=user, **default)
#     return recipe
#
#
# def create_user(**params):
#     return User.objects.create_user(**params)
#
#
# class PublicRecipeApiTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_auth_required(self):
#         res = self.client.get(RECIPES_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateRecipeApiTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = create_user(email="user@exaple.com", password="passwordtest")
#         self.client.force_authenticate(self.user)
#
#     def test_retrieve_recipes(self):
#         create_recipe(user=self.user)
#         create_recipe(user=self.user)
#
#         res = self.client.get(RECIPES_URL)
#         recipe = Recipe.objects.all().order_by("-id")
#         serializer = RecipeSerializer(recipe, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
#
#     def test_recipe_list_limited_to_user(self):
#         other_user = create_user(email="other@example.com", password="passwordtest")
#         create_recipe(user=other_user)
#         create_recipe(user=self.user)
#
#         res = self.client.get(RECIPES_URL)
#         recipe = Recipe.objects.filter(user=self.user)
#         serializer = RecipeSerializer(recipe, may=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
#
#     def test_get_recipe_detail(self):
#         recipe = create_recipe(user=self.user)
#
#         url = detail_url(recipe.id)
#         res = self.client.get(url)
#
#         serializer = RecipeSerializer(recipe)
#         self.assertEqual(res.data, serializer.data)
#
#     def test_create_recipe(self):
#         payload = {"title": "Simple recipe", "time_minutes": 30, "price": Decimal("5.99")}
#         res = self.client.post(RECIPES_URL, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipe = Recipe.objects.get(id=res.data["id"])
#         for k, v in payload.items():
#             self.assertEqual(getattr(recipe, k), v)
#
#         self.assertEqual(recipe.user, self.user)
#
#     def test_update_recipe(self):
#         original_link = "https://example.com/recipe.pdf"
#         recipe = create_recipe(user=self.user, title="Simple recipe title", link=original_link)
#         payload = {"title": "New recipe title"}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         recipe.refresh_from_db()
#         self.assertEqual(recipe.title, payload["title"])
#         self.assertEqual(recipe.link, original_link)
#         self.assertEqual(recipe.user, self.user)
#
#     def test_full_update_recipe(self):
#         recipe = create_recipe(
#             user=self.user,
#             title="Simple recipe title",
#             link="http://example.com/recipe.pdf",
#             description="Simple description",
#         )
#         payload = {
#             "title": "New recipe title",
#             "link": "https://example.com/recipe.pdf",
#             "description": "New recipe  description",
#             "time_minutes": 30,
#             "price": Decimal(5.99),
#         }
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         recipe.refresh_from_db()
#         for k, v in payload.items():
#             self.assertEqual(getattr(recipe, k), v)
#         self.assertEqual(recipe.user, self.user)
#
#     def test_update_user_returns_error(self):
#         new_user = create_user(email="user2@example.com", password="passwordtest")
#         recipe = create_recipe(user=self.user)
#
#         payload = {
#             "user": new_user.id,
#         }
#         url = detail_url(recipe.id)
#         self.client.patch(url, payload)
#         recipe.refresh_from_db()
#         self.assertEqual(recipe.user, self.user)
#
#     def test_delete_recipe(self):
#         recipe = create_recipe(user=self.user)
#         url = detail_url(recipe.id)
#         res = self.client.delete(url)
#
#         self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
#
#     def test_delete_other_user_recipe_error(self):
#         new_user = create_user(email="user2@example.com", password="passwordtest")
#         recipe = create_recipe(user=new_user)
#
#         url = detail_url(recipe.id)
#         res = self.client.delete(url)
#         self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
#
#     def test_create_recipe_with_new_tags(self):
#         payload = {
#             "title": "Thai Prawn Curry",
#             "time_minutes": 30,
#             "price": Decimal(5.99),
#             "tags": [{"name": "Thai"}, {"name": "Dinner"}],
#         }
#         res = self.client.post(RECIPES_URL, payload, format="json")
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)
#         self.assertEqual(recipes.count(), 1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.tags.count(), 2)
#         for tag in payload["tags"]:
#             exists = recipe.tags.filter(
#                 name=tag["name"],
#                 user=self.user,
#             ).exists()
#             self.assertTrue(exists)
#
#     def test_create_recipe_with_existing_tags(self):
#         tag_indian = Tag.objects.create(user=self.user, name="Indian")
#         payload = {
#             "title": "Pongal",
#             "time_minutes": 30,
#             "price": Decimal(5.99),
#             "tags": [{"name": "Indian"}, {"name": "Breakefast"}],
#         }
#         res = self.client.post(RECIPES_URL, payload, format="json")
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)
#         self.assertEqual(recipes.count(), 1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.tags.count(), 2)
#         self.assertEqual(tag_indian, recipe.tags.all())
#         for tag in payload["tags"]:
#             exists = recipe.tags.filter(
#                 name=tag["name"],
#                 user=self.user,
#             ).exists()
#             self.assertTrue(exists)
#
#     def test_create_tag_on_update(self):
#         recipe = create_recipe(user=self.user)
#         payload = {"tags": [{"name": "Lunch"}]}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload, format="json")
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         new_tag = Tag.objects.get(user=self.user, name="Lunch")
#         self.assertIn(new_tag, recipe.tags.all())
#
#     def test_update_recipe_assign_tag(self):
#         tag_breakfast = Tag.objects.create(user=self.user, name="Breakefast")
#         recipe = create_recipe(user=self.user)
#         recipe.tags.add(tag_breakfast)
#
#         tag_lunch = Tag.objects.create(user=self.user, nama="Lunch")
#         payload = {"tags": [{"name": "Lunch"}]}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload, format="json")
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn(tag_lunch, recipe.tags.all())
#         self.assertNotIn(tag_breakfast, recipe.tags.all())
#
#     def test_clear_recipe_tags(self):
#         tag = Tag.objects.create(user=self.user, name="Dessert")
#         recipe = create_recipe(user=self.user)
#         recipe.tags.add(tag)
#
#         payload = {"tags": []}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload, format="json")
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn(recipe.tags.count(), 0)
#
#     def test_create_recipe_with_new_ingredients(self):
#         payload = {
#             "title": "Cauliflower Tacos",
#             "time_minutes": 30,
#             "price": Decimal("4.30"),
#             "ingredients": [{"name": "cauliflower"}, {"name": "salt"}],
#         }
#         res = self.client.post(RECIPES_URL, payload, format="json")
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)
#         self.assertEqual(recipes.count(), 1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.ingredients.count(), 2)
#         for ingredient in payload["ingredients"]:
#             exists = recipe.igredients.filter(
#                 name=ingredient["name"],
#                 user=self.user,
#             ).exists()
#             self.assertTrue(exists)
#
#     def test_create_recipe_with_existing_ingredients(self):
#         ingredient = Ingredient.objects.create(user=self.user, name="Lemon")
#         payload = {
#             "title": "Vietnamese Soup",
#             "time_minutes": 25,
#             "price": "2.55",
#             "ingredients": [{"name": "Lemon"}, {"name": "Fish Sauce"}],
#         }
#         res = self.client.post(RECIPES_URL, payload, format="json")
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)
#         self.assertEqual(recipes.count(), 1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.ingredients.count(), 2)
#         self.assertIn(ingredient, recipe.ingredients.all())
#         for ingredient in payload["ingredients"]:
#             exists = recipe.ingredients.filter(
#                 name=ingredient["name"],
#                 user=self.user,
#             ).exists()
#             self.assertTrue(exists)
#
#     def test_create_ingredient_on_update(self):
#         recipe = create_recipe(user=self.user)
#         payload = {"ingredients": [{"name": "Limes"}]}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload, format="json")
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         new_ingredient = Ingredient.objects.get(user=self.user, name="Limes")
#         self.assertIn(new_ingredient, recipe.ingredients.all())
#
#     def test_update_recipe_assign_ingredient(self):
#         ingredient1 = Ingredient.objects.create(user=self.user, name="Pepper")
#         recipe = create_recipe(user=self.user)
#         recipe.ingredients.add(ingredient1)
#
#         ingredient2 = Ingredient.objects.create(user=self.user, name="Chill")
#         payload = {"ingredients": [{"name": "Chill"}]}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload, format="json")
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn(ingredient1, recipe.ingredients.all())
#         self.assertIn(ingredient2, recipe.ingredients.all())
#
#     def test_clear_recipe_ingredients(self):
#         ingredient = Ingredient.objects.create(user=self.user, name="Garlic")
#         recipe = create_recipe(user=self.user)
#         recipe.ingredients.add(ingredient)
#         payload = {"ingredients": []}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload, format="json")
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(recipe.ingredients.count(), 0)
#
#     def test_filter_by_tags(self):
#         r1 = create_recipe(user=self.user, title="Thai Vegetable Curry")
#         r2 = create_recipe(user=self.user, title="Aubergine, with Tahini")
#         tag1 = Tag.objects.create(user=self.user, name="Vegan")
#         tag2 = Tag.objects.create(user=self.user, name="Vegetarian")
#         r1.tags.add(tag1)
#         r2.tags.add(tag2)
#
#         r3 = create_recipe(user=self.user, title="Fish and Chips")
#         params = {"tags": f"{tag1.id},{tag2.id}"}
#         res = self.client.get(RECIPES_URL, params)
#
#         s1 = RecipeSerializer(r1)
#         s2 = RecipeSerializer(r2)
#         s3 = RecipeSerializer(r3)
#         self.assertIn(s1.data, res.data)
#         self.assertIn(s2.data, res.data)
#         self.assertIn(s3.data, res.data)
#
#     def test_filter_by_ingredients(self):
#         r1 = create_recipe(user=self.user, title="Thai Vegetable Curry")
#         r2 = create_recipe(user=self.user, title="Aubergine, with Tahini")
#
#         in1 = Ingredient.objects.create(user=self.user, name="Feta cheeses")
#         in2 = Ingredient.objects.create(user=self.user, name="Chicken")
#         r1.ingredients.add(in1)
#         r2.ingredients.add(in2)
#         r3 = create_recipe(user=self.user, title="Red Lentil Daal")
#
#         params = {"ingredients": f"{in1.id},{in2.id}"}
#         res = self.client.get(RECIPES_URL, params)
#
#         s1 = RecipeSerializer(r1)
#         s2 = RecipeSerializer(r2)
#         s3 = RecipeSerializer(r3)
#         self.assertIn(s1.data, res.data)
#         self.assertIn(s2.data, res.data)
#         self.assertIn(s3.data, res.data)
#
#
# class ImageUploadTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user("user@example.com", "passwordtest")
#
#     def tearDown(self):
#         self.recipe.image.delete()
#
#     def test_upload_image(self):
#         url = image_upload_url(self.recipe.id)
#         with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
#             img = Image.new("RGB", (10, 10))
#             img.save(image_file, format="JPEG")
#             image_file.seek(0)
#             payload = {"image": image_file}
#             res = self.client.post(url, payload, format="multipart")
#
#         self.recipe.refresh_from_db()
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn("image", res.data)
#         self.assertTrue(os.path.exists(self.recipe.image.path))
#
#     def test_upload_image_bad_request(self):
#         url = image_upload_url(self.recipe.id)
#         payload = {"image": "notanimage"}
#         res = self.client.post(url, payload, format="multipart")
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

# from decimal import Decimal
# from unittest import TestCase
#
# from django.urls import reverse
# from recipes.models import Recipe
# from rest_framework import status
# from rest_framework.test import APIClient
# from users.models import User
#
# from tags.models import Tag
# from tags.serialziers import TagSerializer
#
# TAGS_URL = reverse("tags:tag-list")
#
#
# def detail_url(tag_id):
#     return reverse("tags:tag-detail", args=[tag_id])
#
#
# def create_user(email="user@example.com", password="passwordtest"):
#     return User.objects.create_user(email=email, pasword=password)
#
#
# class PublicTagsApiTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_auth_required(self):
#         res = self.client.get(TAGS_URL)
#         res.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateTagsApiClient(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = create_user()
#         self.client.force_authenticate(user=self.user)
#
#     def test_retrieve_tags(self):
#         Tag.objects.create(user=self.user, name="Vegan")
#         Tag.objects.create(user=self.user, name="Vegetarian")
#
#         res = self.client.get(TAGS_URL)
#         tags = Tag.objects.all().order_by("-name")
#         serializer = TagSerializer(tags, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
#
#     def test_tags_limited_to_user(self):
#         user2 = create_user(email="user@example.com")
#         Tag.objects.create(user=user2, name="Fruity")
#         tag = Tag.objects.create(user=self.user, name="Comfort Food")
#
#         res = self.client.get(TAGS_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.data), 1)
#         self.assertEqual(res.data[0]["name"], tag.name)
#         self.assertEqual(res.data[0]["id"], tag.id)
#
#     def test_update_tag(self):
#         tag = Tag.objects.create(user=self.user, name="After Dinner")
#
#         payload = {"name": "Dessert"}
#         url = detail_url(tag.id)
#         res = self.client.patch(url, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         tag.refresh_from_db()
#         self.assertEqual(tag.name, payload["name"])
#
#     def test_delete_tag(self):
#         tag = Tag.objects.create(user=self.user, name="Breakfast")
#         url = detail_url(tag.id)
#         res = self.client.delete(url)
#
#         self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
#         tags = Tag.objects.filter(user=self.user)
#         self.assertFalse(tags.exists())
#
#     def test_filter_tags_assigned_to_recipes(self):
#         tag1 = Tag.objects.create(user=self.user, name="Breakfast")
#         tag2 = Tag.objects.create(user=self.user, name="Lunch")
#         recipe = Recipe.objects.create(title="Green Eggs", time_minutes=10, price=Decimal("2.50"), user=self.user)
#         recipe.tags.add(tag1)
#         res = self.client.get(TAGS_URL, {"assigned_only": 1})
#         s1 = TagSerializer(tag1)
#         s2 = TagSerializer(tag2)
#         self.assertIn(s1.data, res.data)
#         self.assertNotIn(s2.data, res.data)
#
#     def test_filtered_tags_unique(self):
#         tag = Tag.objects.create(user=self.user, name="Breakfast")
#         Tag.objects.create(user=self.user, name="Dinner")
#
#         recipe1 = Recipe.objects.create(title="Pancakes", time_minutes=10, price=Decimal("2.50"), user=self.user)
#         recipe2 = Recipe.objects.create(title="Porridge", time_minutes=3, price=Decimal("2.50"), user=self.user)
#         recipe1.tags.add(tag)
#         recipe2.tags.add(tag)
#
#         res = self.client.get(TAGS_URL, {"assigned_only": 1})
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.data), 1)

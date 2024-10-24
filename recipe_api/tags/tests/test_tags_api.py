from decimal import Decimal

import pytest
from django.urls import reverse
from recipes.models import Recipe
from rest_framework import status
from users.models import User

from tags.models import Tag
from tags.serialziers import TagSerializer

TAGS_URL = reverse("tags:tag-list")


def detail_url(tag_id):
    return reverse("tags:tag-detail", args=[tag_id])


@pytest.mark.django_db
class TestPublicTagsApi:
    def test_auth_required(self, client):
        res = client.get(TAGS_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateTagsApi:
    def test_retrieve_tags(self, client, create_user):
        client.force_authenticate(create_user)
        Tag.objects.create(user=create_user, name="Vegan")
        Tag.objects.create(user=create_user, name="Vegetarian")

        res = client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_tags_limited_to_user(self, client, create_user):
        client.force_authenticate(create_user)
        user2 = User.objects.create_user(email="user2@example.com", password="passwordtest")
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=create_user, name="Comfort Food")

        res = client.get(TAGS_URL)

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        assert res.data[0]["name"] == tag.name
        assert res.data[0]["id"] == tag.id

    def test_update_tag(self, client, create_user):
        client.force_authenticate(create_user)
        tag = Tag.objects.create(user=create_user, name="After Dinner")

        payload = {"name": "Dessert"}
        url = detail_url(tag.id)
        res = client.patch(url, payload)

        assert res.status_code == status.HTTP_200_OK
        tag.refresh_from_db()
        assert tag.name == payload["name"]

    def test_update_tag_not_owned(self, client, create_user):
        client.force_authenticate(create_user)
        other_user = User.objects.create_user(email="user2@examplee", password="passwordtest")
        tag = Tag.objects.create(user=other_user, name="Dessert")

        payload = {"name": "Dessert"}
        url = detail_url(tag.id)
        res = client.patch(url, payload)
        assert res.status_code == status.HTTP_404_NOT_FOUND
        tag.refresh_from_db()
        assert tag.name == payload["name"]

    def test_delete_tag(self, client, create_user):
        client.force_authenticate(create_user)
        tag = Tag.objects.create(user=create_user, name="Breakfast")
        url = detail_url(tag.id)
        res = client.delete(url)

        assert res.status_code == status.HTTP_204_NO_CONTENT
        tags = Tag.objects.filter(user=create_user)
        assert not tags.exists()

    def test_delete_ingredient_not_owned(self, client, create_user):
        client.force_authenticate(create_user)
        other_user = User.objects.create_user(email="user2@examplee", password="passwordtest")
        tag = Tag.objects.create(user=other_user, name="Breakfast")

        url = detail_url(tag.id)
        res = client.delete(url)

        assert res.status_code == status.HTTP_404_NOT_FOUND
        tag.refresh_from_db()
        assert tag is not None

    def test_filter_tags_assigned_to_recipes(self, client, create_user):
        client.force_authenticate(create_user)
        tag1 = Tag.objects.create(user=create_user, name="Breakfast")
        tag2 = Tag.objects.create(user=create_user, name="Lunch")

        recipe = Recipe.objects.create(title="Green Eggs", time_minutes=10, price=Decimal("2.50"), user=create_user)
        recipe.tags.add(tag1)
        res = client.get(TAGS_URL, {"assigned_only": 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        assert s1.data in res.data
        assert s2.data not in res.data

    def test_filtered_tags_unique(self, client, create_user):
        client.force_authenticate(create_user)
        tag = Tag.objects.create(user=create_user, name="Breakfast")
        Tag.objects.create(user=create_user, name="Dinner")

        recipe1 = Recipe.objects.create(title="Pancakes", time_minutes=10, price=Decimal("2.50"), user=create_user)
        recipe2 = Recipe.objects.create(title="Porridge", time_minutes=3, price=Decimal("2.50"), user=create_user)
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = client.get(TAGS_URL, {"assigned_only": 1})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1

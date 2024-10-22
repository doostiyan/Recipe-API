from django.test import TestCase
from users.models import User

from tags import models


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return User.objects.create_user(email, password)


class TestTag(TestCase):
    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="Tag1")
        self.assertEqual(str(tag), tag.name)

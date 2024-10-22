import pytest

from tags import models


@pytest.mark.django_db
class TestTag:
    def test_create_tag(self, create_user):
        tag = models.Tag.objects.create(user=create_user, name="Tag1")
        assert tag.name == "Tag1"

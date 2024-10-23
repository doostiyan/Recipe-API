import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestAdminSite:
    def test_users_listed(self, client, create_admin_user, create_user):
        url = reverse("admin:users_user_changelist")
        res = client.get(url)

        assert create_user.name in res.content.decode()
        assert create_user.email in res.content.decode()

    def test_edit_user_page(self, client, create_admin_user, create_user):
        url = reverse("admin:users_user_change", args=[create_user.id])
        res = client.get(url)

        assert res.status_code == 200

    def test_create_user_page(self, client, create_admin_user):
        url = reverse("admin:users_user_add")
        res = client.get(url)

        assert res.status_code == 200

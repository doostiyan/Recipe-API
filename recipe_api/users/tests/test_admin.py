from django.test import Client, TestCase
from django.urls import reverse

from users.models import User


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(email="email@example.com", password="passwordtest")
        self.client.force_login(self.admin_user)
        self.user = User.objects.create_user(email="test@example.com", pasword="passwordtest", name="test name")

    def test_users_listed(self):
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

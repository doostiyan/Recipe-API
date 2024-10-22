from unittest import TestCase

from users.models import User


def create_user(email="user@example.com", password="passwordtest"):
    return User.objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "email@example.com"
        password = "passwordtest"
        user = User.objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["TEST2@EXAMPLE.com", "Test2@example.com"],
            ["test3@EXAMPLE.COM", "test3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = User.objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user("", "test123")

    def test_create_new_superuser(self):
        user = User.objects.create_superuser("test@example.com", "passwordtest")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # def test_create_recipe(self):
    #     user = User.objects.create_user(
    #         'test@example.com',
    #         'passwordtest'
    #     )
    #     recipe = models.Recipe.objects.create(
    #
    #     )

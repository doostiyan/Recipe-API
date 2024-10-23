import pytest

from users.models import User


@pytest.mark.django_db
class TestUsers:
    def test_create_user_with_email_successful(self):
        email = "email@example.com"
        password = "passwordtest"
        user = User.objects.create_user(
            email=email,
            password=password,
        )

        assert user.email == email
        assert user.check_password(password)

    def test_new_user_email_normalized(self):
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = User.objects.create_user(email, "sample123")
            assert user.email == expected

    def test_new_user_without_email_raises_error(self):
        with pytest.raises(ValueError):
            User.objects.create_user("", "test123")

    def test_create_new_superuser(self):
        user = User.objects.create_superuser("test@example.com", "passwordtest")
        assert user.is_superuser
        assert user.is_staff

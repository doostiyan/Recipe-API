import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User

CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")
ME_URL = reverse("users:me")


@pytest.mark.django_db
class TestPublicUserApi:
    def test_create_user_success(self, client, create_user_param):
        payload = {"email": "test@example.com", "password": "passwordtest", "name": "test name"}
        res = client.post(CREATE_USER_URL, payload)
        print("Response data:", res.data)
        assert res.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email=payload["email"])

        print("User email:", user.email)
        print("User password check:", user.check_password(payload["password"]))

        assert user.check_password(payload["password"])

    def test_user_with_email_exists_error(self, client, create_user_param):
        payload = {"email": "test@example.com", "password": "passwordtest", "name": "test name"}
        create_user_param(**payload)
        res = client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_short(self, client, create_user_param):
        payload = {"email": "test@examle.com", "password": "pas", "name": "test name"}
        res = client.post(CREATE_USER_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        user_exists = User.objects.filter(email=payload["email"]).exists()
        assert not user_exists

    def test_create_token_for_user(self, client, create_user_param):
        user_detail = {"email": "test@example.com", "password": "passwordtest", "name": "test name"}
        create_user_param(**user_detail)
        payload = {"email": user_detail["email"], "password": user_detail["password"]}
        res = client.post(TOKEN_URL, payload)

        assert "token" in res.data
        assert res.status_code == status.HTTP_200_OK

    def test_create_token_bad_credentials(self, client, create_user_param):
        create_user_param(email="test@examle.com", password="passwordtest")
        payload = {"email": "test@example.com", "password": "passwordtest1"}
        res = client.post(TOKEN_URL, payload)
        assert "token" not in res.data
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_token_blank_password(self, client, create_user_param):
        payload = {
            "email": "test@example.com",
            "password": "",
        }
        res = client.post(TOKEN_URL, payload)
        assert "token" not in res.data
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_user_unauthorized(self, client):
        res = client.get(ME_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateUserApi:
    def test_retrieve_profile_success(self, client, create_user):
        client.force_authenticate(create_user)
        res = client.get(ME_URL)
        assert res.status_code == status.HTTP_200_OK
        assert res.data == {"name": create_user.name, "email": create_user.email}

    def test_post_me_not_allowed(self, client, authenticated_client):
        res = client.post(ME_URL, {})
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_user_profile(self, client, create_user):
        client.force_authenticate(create_user)
        payload = {"name": "new name", "password": "newpassword"}
        res = client.patch(ME_URL, payload)

        create_user.refresh_from_db()
        assert create_user.name == payload["name"]
        assert create_user.check_password(payload["password"])
        assert res.status_code == status.HTTP_200_OK

# from unittest import TestCase
#
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
#
# from users.models import User
#
# CREATE_USER_URL = reverse("users:create")
# TOKEN_URL = reverse("users:token")
# ME_URL = reverse("users:me")
#
#
# def create_user(**params):
#     return User.objects.create_user(**params)
#
#
# class PublicUserApiTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_create_user_success(self):
#         payload = {"email": "test@example.com", "password": "passwordtest", "name": "test name"}
#         res = self.client.post(CREATE_USER_URL, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         user = User.objects.get(email=payload["email"])
#         self.assertTrue(user.check_password(payload["password"]))
#         self.assertNotIn("password", res.data)
#
#     def test_user_with_email_exists_error(self):
#         payload = {"email": "test@example.com", "password": "passwordtest", "name": "test name"}
#         create_user(**payload)
#         res = self.client.post(CREATE_USER_URL, payload)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_password_too_short(self):
#         payload = {"email": "test@examle.com", "password": "pas", "name": "test name"}
#         res = self.client.post(CREATE_USER_URL, payload)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         user_exists = User.objects.filter(email=payload["email"]).exists()
#         self.assertFalse(user_exists)
#
#     def test_create_token_for_user(self):
#         user_detail = {"email": "test@example.com", "password": "passwordtest", "name": "test name"}
#         create_user(**user_detail)
#         payload = {"email": user_detail["email"], "password": user_detail["password"]}
#         res = self.client.post(TOKEN_URL, payload)
#         self.assertIn("token", res.data)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#     def test_create_token_bad_credentials(self):
#         create_user(email="test@examle.com", password="passwordtest")
#         payload = {"email": "test@example.com", "password": "passwordtest1"}
#         res = self.client.post(TOKEN_URL, payload)
#         self.assertNotIn("token", res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_create_token_blank_password(self):
#         payload = {
#             "email": "test@example.com",
#             "password": "",
#         }
#         res = self.client.post(TOKEN_URL, payload)
#         self.assertNotIn("token", res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_retrieve_user_unauthorized(self):
#         res = self.client.get(ME_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateUserApiTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = create_user(email="email@example.com", password="passwordtest", name="test name")
#         self.client.force_authenticate(user=self.user)
#
#     def test_retrieve_profile_success(self):
#         res = self.client.get(ME_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})
#
#     def test_post_me_not_allowed(self):
#         res = self.client.post(ME_URL, {})
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_update_user_profile(self):
#         payload = {"name": "new name", "password": "newpassword"}
#         res = self.client.patch(ME_URL, payload)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.name, payload["name"])
#         self.assertTrue(self.user.check_password(payload["password"]))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

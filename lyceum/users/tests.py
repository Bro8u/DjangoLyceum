from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
import mock
import django.utils.timezone
import pytz

import users.models


__all__ = ["TestUserActivation"]


class TestUserActivation(TestCase):
    def test_with_login(self):
        client = Client()
        client.login(username="temporary", password="temporary")
        client.get("/auth/profile/")

    @mock.patch("users.views.now")
    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE="False")
    def test_user_activate_user_error(self, mock_now):
        django.test.Client().post(
            reverse("users:signup"),
            data={
                "username": "user",
                "mail": "user@user.me",
                "password1": "Q12w3ers",
                "password2": "Q12w3ers",
            },
            follow=True,
        )

        user = users.models.User.objects.get(username="user")
        self.assertFalse(user.is_active)

        mock_now.return_value = pytz.UTC.localize(
            django.utils.timezone.datetime.now() + timedelta(hours=12),
        )

        django.test.Client().get(
            reverse(
                "users:activate_user",
                args=[user.id],
            ),
            follow=True,
        )

        user = users.models.User.objects.get(username="user")
        self.assertFalse(user.is_active)

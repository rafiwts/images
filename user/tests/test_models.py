from django.contrib.auth import get_user_model
from django.test import TestCase

from user.models import AccountTier


class YourModelTestCase(TestCase):
    def test_model(self):
        user = get_user_model().objects.create(
            username="user@example.com", password="password"
        )
        basic_tier = AccountTier.objects.get(name="Basic")
        user.account_tier = basic_tier

        assert user.username == "user@example.com"
        assert user.password == "password"
        assert user.account_tier.name == "Basic"

    # TODO: add test cases and fixtures

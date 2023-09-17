from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    account_tier = models.ForeignKey(
        "AccountTier", on_delete=models.SET_NULL, null=True, related_name="users"
    )

    def __str__(self):
        return self.username


class AccountTier(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

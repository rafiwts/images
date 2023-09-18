from django.contrib.auth.models import AbstractUser
from django.db import models

from image.models import ThumbnailType


class User(AbstractUser):
    account_tier = models.ForeignKey(
        "AccountTier", on_delete=models.SET_NULL, null=True, related_name="users"
    )

    def __str__(self):
        return self.username


class AccountTier(models.Model):
    name = models.CharField(max_length=50)
    thumbnail_size = models.ManyToManyField(ThumbnailType, blank=True)
    link_to_uploaded_file = models.BooleanField(default=False)
    is_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name

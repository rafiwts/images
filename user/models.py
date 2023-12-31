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
    name = models.CharField(max_length=50, unique=True)
    thumbnail_height = models.ManyToManyField(ThumbnailType, blank=True)
    link_to_uploaded_file = models.BooleanField(
        default=False, verbose_name="Uploaded file"
    )
    is_expiring_link = models.BooleanField(default=False, verbose_name="Expiring link")

    def __str__(self):
        return self.name

    @property
    def get_thumbnail_height(self):
        thumbnail_height = self.thumbnail_height.all()
        return thumbnail_height

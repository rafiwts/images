from django.conf import settings
from django.db import models

from .image_handlers import image_name_handler, image_path_handler

User = settings.AUTH_USER_MODEL


class UploadedImage(models.Model):
    # TODO: add a url for an image
    image = models.ImageField(upload_to=image_path_handler)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        file = self.image.name
        file_name = image_name_handler(file)
        return f"{file_name}"


class ThumbnailType(models.Model):
    width = models.IntegerField(models.Model)
    heigth = models.IntegerField(models.Model)

    def __str__(self):
        return f"{self.width}x{self.heigth}"

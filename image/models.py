from django.db import models

from user.models import User

from .handlers import image_name_handler


class UploadedImage(models.Model):
    # TODO: add a url for an image
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        file = self.image.name
        file_name = image_name_handler(file)
        return f"{file_name}"


class ThumbnailType(models.Model):
    width = models.ImageField(models.Model)
    height = models.ImageField(models.Model)

    def __str__(self):
        return f"{self.width}x{self.height}"

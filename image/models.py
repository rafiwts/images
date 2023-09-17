from django.db import models

from user.models import User


class UploadedImage(models.Model):
    # TODO: add a url for an image
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

import os

from django.db import models
from django.dispatch import receiver
from PIL import Image

from .models import Thumbnail, UploadedImage


@receiver(models.signals.post_save, sender=UploadedImage)
def create_thumbnails(sender, instance, created, **kwargs):
    if created:
        if instance.user.account_tier:
            account_tier = instance.user.account_tier
            thumbnails = account_tier.get_thumbnail_height

        thumbnail_heights = []

        for thumbnail in thumbnails:
            thumbnail_heights.append(thumbnail.height)

        # create and save thumbnails for each height available
        for height in thumbnail_heights:
            thumbnail = Thumbnail(
                image=instance,
                thumbnail=resize_image(instance.image, height, instance.user.id),
                user=instance.user,
            )

            thumbnail.save()


def resize_image(image, height, user_id):
    img = Image.open(image.path)

    # resize the image while maintaining aspect ratio
    aspect_ratio = img.width / img.height
    width = int(height * aspect_ratio)

    img.thumbnail((width, height))

    thumbnail_path = (
        f"{user_id}/images/thumbnail_{width}x{height}_{os.path.basename(image.path)}"
    )

    print(thumbnail_path)

    img.save(thumbnail_path, "png")  # You can change the format as needed

    return thumbnail_path

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UploadedImage
from .thumbnail_handlers import change_to_thumbnails


@receiver(post_save, sender=UploadedImage)
async def create_thumbnails(sender, instance: UploadedImage, **kwargs):
    """
    asynchronous implementation enables efficient handling of requests
    """
    await change_to_thumbnails(instance.id)

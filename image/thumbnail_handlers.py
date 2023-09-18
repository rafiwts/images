from .image_handlers import image_name_handler
from .models import UploadedImage


def change_to_thumbnails(pk):
    instance = UploadedImage.objects.get(id=pk)
    account_tier = instance.user.account_tier
    thumbnails_for_tier = account_tier.get_thumbnail_sizes  # noqa: F841
    image_name = image_name_handler(instance.image.name)  # noqa: F841
    # TODO: think about the implementation of thumbnails from image: Pillow?

from io import BytesIO

from celery import shared_task
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PillowImage

from .image_handlers import image_name_handler
from .models import UploadedImage


@shared_task
def change_to_thumbnails(pk):
    # TODO: celery to docker
    instance = UploadedImage.objects.get(id=pk)
    account_tier = instance.user.account_tier
    thumbnails_for_tier = account_tier.get_thumbnail_sizes  # noqa: F841
    image_name = image_name_handler(instance.image.name)  # noqa: F841

    for size in thumbnails_for_tier:
        image_file = BytesIO(instance.image.read())
        uploaded_image = PillowImage.open(image_file)

        thumbnail = uploaded_image.resize(size.width, size.higth)
        thumbnail_io = BytesIO()

        thumbnail.save(thumbnail_io, format="JPEG")

        name = f"{image_name}_{size.width}x{size.heigth}"

        thumbnail_file = SimpleUploadedFile(
            name, thumbnail_io.getvalue(), content_type="image/jpg"
        )

        instance.image.save(name, thumbnail_file, save=False)

import tempfile
from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from PIL import Image
from PIL import Image as PIL_Image

from user.models import AccountTier, ThumbnailType, User


@pytest.fixture
def client(db):
    client = Client()
    return client


@pytest.fixture
def custom_thumbnail_height(db):
    thumbnail = ThumbnailType.objects.create(height=250)

    return thumbnail


@pytest.fixture
def custom_thumbnail_heights(db):
    thumbnail_350 = ThumbnailType.objects.create(height=350)  # noqa: F841
    thumbnail_450 = ThumbnailType.objects.create(height=450)  # noqa: F841


@pytest.fixture
def basic_account_tier(db):
    basic_tier = AccountTier.objects.get(name="Basic")

    return basic_tier


@pytest.fixture
def custom_user(db):
    user = User.objects.create(
        id=5,
        username="user1",
        email="user1@example.com",
        password="user1234!",
    )
    return user


@pytest.fixture
def temporary_image_one():
    size = (200, 200)
    color = (255, 0, 0, 255)
    image = PIL_Image.new("RGBA", size, color)

    # convert
    rgb_image = PIL_Image.new("RGB", image.size)
    rgb_image.paste(image, (0, 0), image)

    temp_file = tempfile.NamedTemporaryFile()

    # save as jpeg
    rgb_image.save(temp_file, "JPEG")
    return temp_file


@pytest.fixture
def temporary_image_two():
    size = (400, 400)
    color = (0, 250, 250, 0)
    image = PIL_Image.new("RGBA", size, color)

    rgb_image = PIL_Image.new("RGB", image.size)
    rgb_image.paste(image, (250, 250), image)

    temp_file = tempfile.NamedTemporaryFile()

    rgb_image.save(temp_file, "JPEG")
    return temp_file


@pytest.fixture
def image_file():
    image = Image.new("RGB", (100, 100))
    image_io = BytesIO()
    image.save(image_io, format="JPEG")
    image_file = SimpleUploadedFile("test_image.jpg", image_io.getvalue())

    return image_file

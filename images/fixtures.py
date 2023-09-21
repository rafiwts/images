import pytest

from user.models import ThumbnailType


@pytest.fixture
def custom_thumbnail_height(db):
    thumbnail = ThumbnailType.objects.create(height=250)

    return thumbnail


@pytest.fixture
def custom_thumbnail_heights(db):
    thumbnail_350 = ThumbnailType.objects.create(height=350)  # noqa: F841
    thumbnail_450 = ThumbnailType.objects.create(height=450)  # noqa: F841

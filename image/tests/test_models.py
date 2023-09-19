from django.test import TestCase

from image.models import ThumbnailType


class YourModelTestCase(TestCase):
    def test_model(self):
        obj = ThumbnailType.objects.create(width=10, heigth=10)
        assert obj.width == 10

    # TODO: add test cases and fixtures

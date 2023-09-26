import tempfile

import pytest
from django.db.utils import IntegrityError
from django.test import override_settings
from django.utils import timezone
from freezegun import freeze_time

from image.models import Thumbnail, UploadedImage


@pytest.mark.django_db
class TestUploadedImage:
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_uploading_files_and_user(
        self, custom_user, temporary_image_one, temporary_image_two
    ):
        # upload two different for the same user
        mock_image_one = temporary_image_one
        mock_image_two = temporary_image_two
        uploaded_image_one = UploadedImage.objects.create(
            image=mock_image_one.name, user=custom_user
        )
        uploaded_image_two = UploadedImage.objects.create(
            image=mock_image_two.name, user=custom_user
        )

        assert len(UploadedImage.objects.all()) == 2
        assert uploaded_image_one.user.username == custom_user.username
        assert uploaded_image_two.user.username == custom_user.username

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_uploading_file_url(self, custom_user, temporary_image_one):
        mock_image = temporary_image_one

        filepath = f"{mock_image.name}"

        uploaded_image = UploadedImage.objects.create(
            image=mock_image.name, user=custom_user
        )
        image_url = uploaded_image.get_orignal_url

        assert filepath == image_url

    @freeze_time("2023-09-21 12:00:00")
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_uploading_file_date(self, custom_user, temporary_image_one):
        mock_image_one = temporary_image_one

        image_one = UploadedImage.objects.create(
            image=mock_image_one.name, user=custom_user
        )

        assert image_one.uploaded_at == timezone.now()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_image_with_no_corresponding_user(self, temporary_image_one):
        with pytest.raises(IntegrityError):
            mock_image = temporary_image_one
            uploaded_image = UploadedImage.objects.create(image=mock_image.name)
            uploaded_image.save()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_thumbnail_with_corresponding_image(
        self, custom_user, temporary_image_one, temporary_image_two
    ):
        mock_image = temporary_image_one
        mock_thumbnail = temporary_image_two

        uploaded_image = UploadedImage.objects.create(
            image=mock_image.name, user=custom_user
        )
        thumbnail = Thumbnail.objects.create(
            image=uploaded_image,
            thumbnail=mock_thumbnail.name,
            height=200,
            user=custom_user,
        )

        assert uploaded_image.image == thumbnail.image.image
        assert uploaded_image.user == thumbnail.image.user

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_thumbnail_with_no_corresponding_user(
        self, custom_user, temporary_image_one, temporary_image_two
    ):
        with pytest.raises(IntegrityError):
            mock_image = temporary_image_one
            mock_thumbnail = temporary_image_two
            uploaded_image = UploadedImage.objects.create(
                image=mock_image.name, user=custom_user
            )
            thumbnail = Thumbnail.objects.create(
                image=uploaded_image, thumbnail=mock_thumbnail.name
            )
            thumbnail.save()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_thumbnail_with_no_corresponding_image(
        self, custom_user, temporary_image_one
    ):
        with pytest.raises(IntegrityError):
            mock_thumbnail = temporary_image_one
            thumbnail = Thumbnail.objects.create(
                thumbnail=mock_thumbnail.name, user=custom_user
            )
            thumbnail.save()

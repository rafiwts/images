import json
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from image.models import UploadedImage
from user.models import User


class TestApiViews:
    @pytest.mark.django_db
    def test_list_view_link(self, client):
        # get a superuser who has been already created
        client.login(username="image", password="image1234!")
        url = reverse("image-list")
        response = client.get(url)

        assert response.status_code == 200

    @pytest.mark.django_db
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_view(self, client, image_file):
        # FIXME: path issue for thumbnails
        superuser = User.objects.get(username="image")
        client.login(username="image", password="image1234!")
        url = reverse("image-create")

        data = {
            "image": image_file,
        }

        response = client.post(url, data, format="multipart")

        assert response.status_code == 201
        assert UploadedImage.objects.count() == 1
        assert UploadedImage.objects.filter(user=superuser).count() == 1

    @pytest.mark.django_db
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_view_with_invalid_file(self, client, image_file):
        invalid_file = SimpleUploadedFile("test_file.txt", b"file_content")

        # FIXME: path issue for thumbnails
        client.login(username="image", password="image1234!")
        url = reverse("image-create")

        data = {
            "image": image_file,
        }
        response = client.post(url, data, format="multipart")

        assert response.status_code == 201

        data = {"image": invalid_file}
        response = client.post(url, data)

        assert response.status_code == 400

    @pytest.mark.django_db
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_list_view_response_return(self, client, image_file):
        # create an image
        client.login(username="image", password="image1234!")
        url = reverse("image-create")

        data = {
            "image": image_file,
        }
        client.post(url, data, format="multipart")

        url = reverse("image-list")
        response = client.get(url)

        assert response.status_code == 200

        # get the image on the api list
        url = reverse("image-list")
        response = client.get(url)

        parsed_data = json.loads(response.content.decode("utf-8"))

        assert response.status_code == 200
        assert len(parsed_data) == 1

    @pytest.mark.django_db
    def test_list_view_with_no_user_logged_in(self, client):
        # it should return a TypeError as no id has been provided
        with pytest.raises(TypeError):
            url = reverse("image-list")
            response = client.get(url)
            assert response.status_code == 200

    # TODO: test for thumbnail after resolving the path issue - the test throws an error

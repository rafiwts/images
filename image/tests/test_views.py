import json
import tempfile

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from image.handlers import generate_link_handler
from image.models import ExpiringLinkAccess, UploadedImage
from user.models import User


@pytest.mark.django_db
class TestApiViews:
    def test_image_list_view(self, client):
        # get a superuser who has been already created
        client.login(username="image", password="image1234!")
        url = reverse("image-list")
        response = client.get(url)

        assert response.status_code == 200

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_image_view(self, client, image_file):
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

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_image_view_with_invalid_file(self, client, image_file):
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

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_image_list_view_response_return(self, client, image_file):
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

    def test_list_view_with_no_user_logged_in(self, client):
        # it should return a TypeError as no id has been provided
        with pytest.raises(TypeError):
            url = reverse("image-list")
            response = client.get(url)
            assert response.status_code == 200

    def test_expiring_links_list_with_authorized_user(self, client):
        # get a user with right to fetch an expiring link
        client.login(username="enterprise", password="enterprise1234!")
        url = reverse("link-list")
        response = client.get(url)

        assert response.status_code == 200

    def test_expiring_links_list_with_unauthorized_user(self, client):
        # get a user with no rights to fetch an expiring link
        client.login(username="basic", password="basic1234!")
        url = reverse("link-list")
        response = client.get(url)

        assert response.status_code == 400

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_link_view_with_authorized_user(self, client, image_file):
        # FIXME: path issue for thumbnails, it creates thumbnails while testing
        superuser = User.objects.get(username="enterprise")
        image = UploadedImage.objects.create(image=image_file, user=superuser)
        client.login(username="enterprise", password="enterprise1234!")

        url = reverse("create-link")

        data = {"image": image.id, "expiration_time": 3000}

        response = client.post(url, data)

        assert response.status_code == 201
        assert ExpiringLinkAccess.objects.count() == 1
        assert ExpiringLinkAccess.objects.filter(user=superuser).count() == 1

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_link_view_with_invalid_expiration_time(self, client, image_file):
        # FIXME: path issue for thumbnails, it creates thumbnails while testing
        superuser = User.objects.get(username="enterprise")
        image = UploadedImage.objects.create(image=image_file, user=superuser)
        client.login(username="enterprise", password="enterprise1234!")

        url = reverse("create-link")

        data = {"image": image.id, "expiration_time": 20}

        response = client.post(url, data)

        parsed_data = json.loads(response.content.decode("utf-8"))
        exception_content = parsed_data["expiration_time"][0]

        assert response.status_code == 400
        assert exception_content == "Value must be between 300 and 30000."

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_link_view_with_unauthorized_user(self, client, image_file):
        superuser = User.objects.get(username="basic")
        image = UploadedImage.objects.create(image=image_file, user=superuser)
        client.login(username="basic", password="basic1234!")

        url = reverse("create-link")

        data = {"image": image.id, "expiration_time": 3000}

        response = client.post(url, data)

        # forbidden for unauthorized users
        assert response.status_code == 403

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_link_detail_view(self, client, image_file):
        superuser = User.objects.get(username="enterprise")
        image = UploadedImage.objects.create(image=image_file, user=superuser)
        client.login(username="enterprise", password="enterprise1234!")

        url = reverse("create-link")

        data = {"image": image.id, "expiration_time": 3000}

        response = client.post(url, data)

        expiring_link = ExpiringLinkAccess.objects.get(image=image)
        link = generate_link_handler(response.wsgi_request, expiring_link.link_id)

        response = client.get(link)

        # created url redirects to a link with an image
        assert response.status_code == 301

    # FIXME: test for thumbnail after resolving the path issue - the test throws an error

import tempfile

import pytest
from django.test import override_settings
from django.urls import reverse


class TestApiViews:
    @pytest.mark.django_db
    def test_list_view(self, client):
        # get a superuser who has been already created
        client.login(username="image", password="image1234!")
        url = reverse("image-list")
        response = client.get(url)

        assert response.status_code == 200

    @pytest.mark.django_db
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_view(self, client, image_file):
        client.login(username="image", password="image1234!")
        url = reverse("image-create")

        data = {
            "image": image_file,
        }

        response = client.post(url, data, format="multipart")

        assert response.status_code == 201

    @pytest.mark.django_db
    def test_list_view_with_no_user_logged_in(self, client):
        # it should return a TypeError as no id has been provided
        with pytest.raises(TypeError):
            url = reverse("image-list")
            response = client.get(url)
            assert response.status_code == 200

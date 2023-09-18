from django.urls import path

from .views import CreateImageView, ListImageView

urlpatterns = [
    path("list/", ListImageView.as_view(), name="image-list"),
    path("image/", CreateImageView.as_view(), name="image-create"),
]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    CreateExiringLinkView,
    CreateImageView,
    ListExpiringLinkView,
    ListImageView,
    RetrieveExpiringLinkView,
)

urlpatterns = [
    path("images/", ListImageView.as_view(), name="image-list"),
    path("upload-image/", CreateImageView.as_view(), name="image-create"),
    path("expiring-links/", ListExpiringLinkView.as_view(), name="link-list"),
    path("create-link/", CreateExiringLinkView.as_view(), name="create-link"),
    path(
        "link/<str:link_id>/",
        RetrieveExpiringLinkView.as_view(),
        name="link-detail",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

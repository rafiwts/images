from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    CreateImageView,
    ExpiringLinkListCreateView,
    ExpiringLinkRetrieveView,
    ListImageView,
)

urlpatterns = [
    path("images/", ListImageView.as_view(), name="image-list"),
    path("upload-images/", CreateImageView.as_view(), name="image-create"),
    path("expiring-links/", ExpiringLinkListCreateView.as_view(), name="link-list"),
    path(
        "expiring_link/<int:pk>/",
        ExpiringLinkRetrieveView.as_view(),
        name="link-detail",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

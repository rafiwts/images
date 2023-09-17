from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ImageViewSet

router = DefaultRouter()
router.register(prefix="images", viewset=ImageViewSet)

urlpatterns = [path("", include(router.urls))]

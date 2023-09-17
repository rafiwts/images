from rest_framework import viewsets

from .models import UploadedImage
from .serializers import UploadedImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    # TODO: add which user should upload an image - now there is no user
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

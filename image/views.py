from rest_framework import generics

from .models import UploadedImage
from .serializers import CreateImageSerializer, ListImageSerializer


class ListImageView(generics.ListAPIView):
    # TODO: add which user should upload an image - now there is no user
    queryset = UploadedImage.objects.all()
    serializer_class = ListImageSerializer

    def get_queryset(self):
        queryset = UploadedImage.objects.filter(user=self.request.user)
        return queryset


class CreateImageView(generics.CreateAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = CreateImageSerializer

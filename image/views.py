from django.core import signing
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.response import Response

from .models import ExpiringLinkAccess, UploadedImage
from .serializers import (
    CreateImageSerializer,
    ListExpiringLinksSerializer,
    ListImageSerializer,
)


class ListImageView(generics.ListAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = ListImageSerializer

    def get_queryset(self):
        queryset = UploadedImage.objects.filter(user=self.request.user)
        return queryset


class CreateImageView(generics.CreateAPIView):
    serializer_class = CreateImageSerializer


class ExpiringLinkRetrieveView(generics.RetrieveAPIView):
    serializer_class = ListExpiringLinksSerializer

    def get(self, request, pk):
        try:
            instance = ExpiringLinkAccess.objects.get(pk=pk)
        except ExpiringLinkAccess.DoesNotExist:
            return HttpResponseBadRequest("Image not found")

        url = signing.dumps({"image_id": instance.id}, salt="expiring-link")

        image_url = request.build_absolute_uri(instance.image.image.url)

        url = image_url
        print(url)
        return HttpResponseRedirect(url)


class ExpiringLinkListCreateView(generics.ListAPIView):
    queryset = ExpiringLinkAccess.objects.all()
    serializer_class = ListExpiringLinksSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = ExpiringLinkAccess.objects.filter(user=user)

        return queryset

    def list(self, request, *args, **kwargs):
        account_tier = self.request.user.account_tier
        print(account_tier)

        if not account_tier or account_tier.is_expiring_link == False:
            error_message = (
                "You do not have permission to access fetch the link to the file."
            )

            return Response(
                {"detail": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

        return super().list(request, *args, **kwargs)

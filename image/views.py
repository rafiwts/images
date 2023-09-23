from django.http import HttpResponseBadRequest, HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.response import Response

from .models import ExpiringLinkAccess, UploadedImage
from .serializers import (
    CreateImageSerializer,
    ExpiringLinkSerializer,
    ListExpiringLinkSerializer,
    ListImageSerializer,
)
from .validators import permission_validation_error


class ListImageView(generics.ListAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = ListImageSerializer

    def get_queryset(self):
        queryset = UploadedImage.objects.filter(user=self.request.user)
        return queryset


class CreateImageView(generics.CreateAPIView):
    serializer_class = CreateImageSerializer


class RetrieveExpiringLinkView(generics.RetrieveAPIView):
    serializer_class = ListExpiringLinkSerializer

    def get(self, request, link_id):
        expiring_link = ExpiringLinkAccess.objects.get(link_id=link_id)

        if expiring_link.has_expired():
            # TODO: it deletes after clicking on it or maybe I shoild not delete it
            expiring_link.delete()
            return HttpResponseBadRequest("The link has already expired")

        image_url = request.build_absolute_uri(expiring_link.image.image.url)
        return HttpResponseRedirect(image_url)


class CreateExiringLinkView(generics.CreateAPIView):
    queryset = ExpiringLinkAccess.objects.all()
    serializer_class = ExpiringLinkSerializer


class ListExpiringLinkView(generics.ListAPIView):
    queryset = ExpiringLinkAccess.objects.all()
    serializer_class = ListExpiringLinkSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = ExpiringLinkAccess.objects.filter(user=user)

        return queryset

    def list(self, request, *args, **kwargs):
        account_tier = self.request.user.account_tier

        if not account_tier or account_tier.is_expiring_link == False:
            return Response(
                {"detail": permission_validation_error()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_list = super().list(request, *args, **kwargs)

        return current_list

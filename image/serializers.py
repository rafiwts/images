import uuid

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .handlers import generate_link_handler
from .models import ExpiringLinkAccess, Thumbnail, UploadedImage


class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ("thumbnail",)


class ListImageSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True, source="thumbnails.all")

    class Meta:
        model = UploadedImage
        fields = (
            "image",
            "thumbnails",
        )

    def to_representation(self, instance):
        account_tier = instance.user.account_tier

        # if the account tier exist - account_tier is not required
        if account_tier:
            if account_tier.link_to_uploaded_file is False:
                representation = super().to_representation(instance)
                representation.pop("image", None)
            else:
                representation = super().to_representation(instance)
        else:
            # if no account tier - only image url will be returned
            representation = super().to_representation(instance)
            representation.pop("thumbnails", None)
        return representation


class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ("image",)

    def create(self, data):
        context = self.context["request"].user
        data["user"] = context
        queryset = UploadedImage.objects.create(**data)

        return queryset


class ListExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLinkAccess
        fields = ("link_id",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context["request"]
        representation["link_id"] = generate_link_handler(
            request, representation["link_id"]
        )

        return representation


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLinkAccess
        fields = ("image", "expiration_time")

    def create(self, data):
        user = self.context["request"].user

        # it does not allow unauthorized users to fetch links
        if not user.account_tier or not user.account_tier.is_expiring_link:
            raise PermissionDenied("You are not authorized to generate custom links")

        data["user"] = user
        data["link_id"] = uuid.uuid4()

        queryset = ExpiringLinkAccess.objects.create(**data)

        return queryset

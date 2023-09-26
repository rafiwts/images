import uuid

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from user.models import AccountTier

from .handlers import generate_link_handler, thumbnails_response_handler
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

        representation = super().to_representation(instance)

        if account_tier:
            # get the response and override it with custom response
            thumbnail_response = representation["thumbnails"]
            thumbnail_heights = account_tier.get_thumbnail_height
            account_tier = AccountTier.objects.get(name=account_tier.name)
            custom_thumbnail_response = thumbnails_response_handler(
                thumbnail_heights, thumbnail_response
            )
            if account_tier.link_to_uploaded_file is False:
                representation = super().to_representation(instance)
                representation.pop("image", None)
                representation["thumbnails"] = custom_thumbnail_response
            else:
                representation = super().to_representation(instance)
                representation["thumbnails"] = custom_thumbnail_response
        else:
            # if no account tier - only image url will be returned
            representation = super().to_representation(instance)
            representation.pop("thumbnails", None)

        print(representation)

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
        fields = ("link",)


class ExpiringLinkSerializer(serializers.ModelSerializer):
    link = serializers.CharField(read_only=True)

    class Meta:
        model = ExpiringLinkAccess
        fields = ("link", "image", "expiration_time")

    def create(self, data):
        user = self.context["request"].user

        # it does not allow unauthorized users to fetch links
        if not user.account_tier or not user.account_tier.is_expiring_link:
            raise PermissionDenied("You are not authorized to generate custom links")

        request = self.context["request"]

        link = generate_link_handler(request, uuid.uuid4())

        data["user"] = user
        data["link"] = link

        # if an image does not belong to a user
        if data["image"].user.id != user.id:
            raise PermissionDenied(
                "You cannot generate links for images that do not belong to you"
            )

        queryset = ExpiringLinkAccess.objects.create(**data)

        return queryset

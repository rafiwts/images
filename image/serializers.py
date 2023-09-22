from rest_framework import serializers

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


class ListExpiringLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLinkAccess
        fields = ("link",)


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLinkAccess
        fields = ("id", "image", "expiration_time", "created_at")
        # TODO: add url for creating a image with a link

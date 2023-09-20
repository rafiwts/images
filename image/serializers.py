from rest_framework import serializers

from .models import Thumbnail, UploadedImage


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

        if account_tier.link_to_uploaded_file is False:
            representation = super().to_representation(instance)
            representation.pop("image", None)
        else:
            representation = super().to_representation(instance)

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

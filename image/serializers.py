from rest_framework import serializers

from .models import UploadedImage


class ListImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ("image", "uploaded_at")


class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ("image",)

    def create(self, data):
        context = self.context["request"].user
        data["user"] = context
        queryset = UploadedImage.objects.create(**data)
        return queryset

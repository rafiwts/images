from django.contrib import admin

from .models import ThumbnailType, UploadedImage

admin.site.register(UploadedImage)
admin.site.register(ThumbnailType)

from django.contrib import admin

from .models import ExpiringLinkAccess, ThumbnailType, UploadedImage


@admin.register(UploadedImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "uploaded_at")
    ordering = ["-uploaded_at"]


admin.site.register(ThumbnailType)
admin.site.register(ExpiringLinkAccess)

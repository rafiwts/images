from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.forms import UserForm
from user.models import AccountTier, User


class CustomUserAccountAdmin(UserAdmin):
    add_form = UserForm
    model = User
    list_display = [
        "username",
        "account_tier",
        "email",
        "is_staff",
    ]
    list_display_links = ["username"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("account_tier",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("account_tier",)}),)


admin.site.register(User, CustomUserAccountAdmin)
admin.site.register(AccountTier)

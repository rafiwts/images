from django.db.models.signals import post_migrate
from django.dispatch import receiver

from image.models import ThumbnailType
from user.models import AccountTier, User


@receiver(post_migrate)
def create_bultin_tiers(sender, **kwargs):
    """
    the signal creates built-in account tiers and builtin thumbnails
    """
    if AccountTier.objects.filter(name="Basic").exists():
        return
    global basic_account
    global premium_account
    global enterprise_account

    # bult-in basic account with thumbnails
    basic_account = AccountTier(
        name="Basic",
        link_to_uploaded_file=False,
        is_expiring_link=False,
    )
    small_thumbmail = ThumbnailType(height=200)
    small_thumbmail.save()
    basic_account.save()
    basic_account.thumbnail_height.add(small_thumbmail)

    # built-in premium account with thumbnails
    premium_account = AccountTier(
        name="Premium",
        link_to_uploaded_file=True,
        is_expiring_link=False,
    )
    large_thumbmail = ThumbnailType(height=400)
    large_thumbmail.save()

    premium_account.save()
    premium_account.thumbnail_height.set([small_thumbmail, large_thumbmail])

    # built-in enterprise account with thumbnails
    enterprise_account = AccountTier(
        name="Enterprise",
        link_to_uploaded_file=True,
        is_expiring_link=True,
    )
    enterprise_account.save()
    enterprise_account.thumbnail_height.set([small_thumbmail, large_thumbmail])


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if User.objects.filter(username="image").exists():
        return

    # create 4 superusers
    User.objects.create_superuser("image", "image@example.com", "image1234!")
    User.objects.create_superuser(
        "basic", "basic@example.com", "basic1234!", account_tier=basic_account
    )
    User.objects.create_superuser(
        "premium", "premium@example.com", "premium1234!", account_tier=premium_account
    )
    User.objects.create_superuser(
        "enterprise",
        "enterprise@example.com",
        "enterprise1234!",
        account_tier=enterprise_account,
    )

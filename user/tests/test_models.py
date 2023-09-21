import pytest

from user.models import AccountTier, User


@pytest.mark.django_db
class TestUser:
    @pytest.mark.parametrize(
        "name, email",
        [
            ("image", "image@example.com"),
            ("basic", "basic@example.com"),
            ("premium", "premium@example.com"),
            ("enterprise", "enterprise@example.com"),
        ],
    )
    def test_existing_superusers(self, name, email):
        superuser = User.objects.get(username=name, email=email)

        assert superuser.username == name
        assert superuser.email == email
        assert superuser.is_active == True
        assert superuser.is_staff == True
        assert superuser.is_superuser == True

    @pytest.mark.parametrize(
        "name, account_tier",
        [("basic", "Basic"), ("premium", "Premium"), ("enterprise", "Enterprise")],
    )
    def test_existing_superusers_with_account_tiers(self, name, account_tier):
        superuser = User.objects.get(username=name)

        assert superuser.account_tier.name == account_tier

    def test_existing_superuser_without_account_tier(self):
        # we cannot give a new attribute to an objects that does not exist
        with pytest.raises(AttributeError):
            superuser = User.objects.get(username="image")
            superuser.account_tier.name = "Basic"

    @pytest.mark.parametrize(
        "name, email, password, account_tier",
        [
            ("basic_user", "basic.user@example.com", "basic1234!", "Basic"),
            ("premium_user", "premium.user@example.com", "premium1234!", "Premium"),
            (
                "enterprise_user",
                "enterprise.user@example.com",
                "enterprise1234!",
                "Enterprise",
            ),
        ],
    )
    def test_create_new_users_with_account_tiers(
        self, name, email, password, account_tier
    ):
        new_account_tier = AccountTier.objects.get(name=account_tier)

        new_user = User.objects.create(
            username=name, email=email, password=password, account_tier=new_account_tier
        )

        assert new_user.username == name
        assert new_user.email == email
        assert new_user.account_tier.name == account_tier
        assert new_user.is_active == True
        assert new_user.is_staff == False
        assert new_user.is_superuser == False

    @pytest.mark.parametrize(
        "account_tier, thumbnail_heights, link_to_file, expiring_link",
        [
            ("Basic", [200], False, False),
            ("Premium", [200, 400], True, False),
            ("Enterprise", [200, 400], True, True),
        ],
    )
    def test_existing_account_tiers_attributes(
        self, account_tier, thumbnail_heights, link_to_file, expiring_link
    ):
        account_tier = AccountTier.objects.get(name=account_tier)

        thumbnail_height_qs = account_tier.get_thumbnail_height
        thumbnail_height_list = [
            thumbnail_height.height for thumbnail_height in thumbnail_height_qs
        ]

        assert thumbnail_height_list == thumbnail_heights
        assert account_tier.link_to_uploaded_file == link_to_file
        assert account_tier.is_expiring_link == expiring_link

    def test_custom_account_tier_attributes_with_one_thumbnail_height(
        self, custom_thumbnail_height
    ):
        custom_account_tier = AccountTier.objects.create(
            name="Custom", link_to_uploaded_file=True, is_expiring_link=False
        )

        thumbnail = custom_thumbnail_height.id
        custom_account_tier.thumbnail_height.set([thumbnail])

        for thumbnail in custom_account_tier.thumbnail_height.all():
            assert thumbnail.height == 250

        assert custom_account_tier.name == "Custom"
        assert custom_account_tier.link_to_uploaded_file == True
        assert custom_account_tier.is_expiring_link == False

    def test_custom_account_tier_attributes_with_one_thumbnail_height(
        self, custom_thumbnail_heights
    ):
        custom_account_tier = AccountTier.objects.create(
            name="Custom", link_to_uploaded_file=False, is_expiring_link=True
        )

        # id for fixtures thumbnails
        custom_account_tier.thumbnail_height.set([3, 4])

        thumnbail_heights = []

        for thumnbail in custom_account_tier.thumbnail_height.all():
            thumnbail_heights.append(thumnbail.height)

        assert thumnbail_heights == [350, 450]
        assert custom_account_tier.name == "Custom"
        assert custom_account_tier.link_to_uploaded_file == False
        assert custom_account_tier.is_expiring_link == True

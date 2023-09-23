from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_expiration_time(value):
    min_value = 300
    max_value = 30000
    if value < min_value or value > max_value:
        raise ValidationError(
            _("Value must be between %(min_value)s and %(max_value)s."),
            params={"min_value": min_value, "max_value": max_value},
        )


def permission_validation_error():
    error_message = "You do not have permission to access fetch the link to the file."

    return error_message

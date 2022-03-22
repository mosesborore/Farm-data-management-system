from django.core.exceptions import ValidationError


def validate_possible_ph_value(ph):
    ph = float(ph)

    if ph and ph > 14.0 or ph < 0.0:
        raise ValidationError("ph values should be a number between 0.0 - 14.0")

    return ph

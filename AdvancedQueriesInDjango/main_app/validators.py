from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Manager
from django.utils.deconstruct import deconstructible


# def validate_rating(value: Decimal):
#     if not (0 <= value <= 10):
#         raise ValidationError("The rating must be between 0.0 and 10.0")

@deconstructible
class RangeValidator:
    def __init__(self, min_value: int | Decimal, max_value: int | Decimal, message: str=None):
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    def __call__(self, value: int | Decimal):
        if not (self.min_value <= value <= self.max_value):
            raise ValidationError(self.message)

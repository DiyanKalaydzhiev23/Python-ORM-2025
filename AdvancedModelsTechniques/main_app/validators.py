import re

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

# Option 1
def validate_name(value: str) -> None:
    for char in value:
        if not (char.isalpha() or char.isspace()):
            raise ValidationError("Name can only contain letters and spaces")

# Option 2
@deconstructible
class NameValidator:
    def __init__(self, message: str):
        self.message = message

    def __call__(self, value: str):
        for char in value:
            if not (char.isalpha() or char.isspace()):
                raise ValidationError(self.message)


@deconstructible
class PhoneNumberValidator:
    def __init__(self, message: str):
        self.message = message

    def __call__(self, value: str):
        if not re.match(r'^\+359\d{9}$', value):
            raise ValidationError(self.message)

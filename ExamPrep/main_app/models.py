from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from main_app.managers import ProfileManager


class DateTime(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )


class Profile(DateTime):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=15,
    )

    address = models.TextField()

    is_active = models.BooleanField(
        default=True,
    )

    objects = ProfileManager()


class Product(DateTime):
    MIN_PRICE: float = 0.01

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(MIN_PRICE),
        ]
    )

    in_stock = models.PositiveIntegerField()

    is_available = models.BooleanField(
        default=True,
    )


class Order(DateTime):
    MIN_TOTAL_PRICE: float = 0.01

    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
    )

    products = models.ManyToManyField(
        to=Product,

    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(MIN_TOTAL_PRICE),
        ]
    )

    is_completed = models.BooleanField(
        default=False,
    )

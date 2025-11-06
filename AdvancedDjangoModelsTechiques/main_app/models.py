from decimal import Decimal

from django.contrib.postgres.search import SearchVectorField
from django.core.validators import RegexValidator, MinValueValidator, MinLengthValidator
from django.db import models

from main_app.mixins import RechargeEnergyMixin
from main_app.validators import NameValidator


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            # Option 1
            # RegexValidator(
            #     regex=r'[A-z ]+ ',
            #     message="Name can only contain letters and spaces",
            # )
            # Option 2
            # validate_name
            # validate_name("Name can only contain letters and spaces"),
            # Option 3
            NameValidator(message="Name can only contain letters and spaces")
        ],
    )

    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                limit_value=18,
                message="Age must be greater than or equal to 18"
            )
        ]
    )

    email = models.EmailField(
        error_messages={'invalid': "Enter a valid email address"},
    )

    phone_number = models.CharField(
        max_length=13,
        validators=[
            # PhoneNumberValidator(
            #     message="Phone number must start with '+359' followed by 9 digits"
            # ),
            RegexValidator(
                regex=r'^\+359\d{9}$',
                message="Phone number must start with '+359' followed by 9 digits",
            )
        ]
    )

    website_url = models.URLField(
        error_messages={'invalid': 'Enter a valid URL'},
    )


class BaseMedia(models.Model):
    title = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    genre = models.CharField(
        max_length=50,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']  # Done on SELECT not on INSERT. Is inherited!


class Book(BaseMedia):
    AUTHOR_MIN_LENGTH_VALUE: int = 5
    AUTHOR_MAX_LENGTH_VALUE: int = 100
    ISBN_MIN_LENGTH_VALUE: int = 6
    ISBN_MAX_LENGTH_VALUE: int = 20

    author = models.CharField(
        max_length=AUTHOR_MAX_LENGTH_VALUE,
        validators=[
            MinLengthValidator(
                limit_value=AUTHOR_MIN_LENGTH_VALUE,
                message=f"Author must be at least {AUTHOR_MIN_LENGTH_VALUE} characters long",
            )
        ],
    )

    isbn = models.CharField(
        max_length=ISBN_MAX_LENGTH_VALUE,
        unique=True,
        validators=[
            MinLengthValidator(
                limit_value=ISBN_MIN_LENGTH_VALUE,
                message=f"ISBN must be at least {ISBN_MIN_LENGTH_VALUE} characters long",
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"



class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=8,
                message="Director must be at least 8 characters long",
            )
        ],
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"




class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=9,
                message="Artist must be at least 9 characters long",
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"


class Product(models.Model):
    TAX_PERCENT: Decimal = Decimal('0.08')
    SHIPPING_MULTIPLIER: Decimal = Decimal('2.00')
    TYPE_PRODUCT: str = "Product"

    name = models.CharField(
        max_length=100,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def calculate_tax(self) -> Decimal:
        return Decimal(str(self.price)) * self.TAX_PERCENT

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return weight * self.SHIPPING_MULTIPLIER

    def format_product_name(self) -> str:
        return f"{self.TYPE_PRODUCT}: {self.name}"


class DiscountedProduct(Product):
    TAX_PERCENT: Decimal = Decimal('0.05')
    SHIPPING_MULTIPLIER: Decimal = Decimal('1.50')
    TYPE_PRODUCT: str = "Discounted Product"
    PRICE_WITHOUT_DISCOUNT_MULTIPLIER = Decimal('0.20')

    def calculate_price_without_discount(self) -> Decimal:
        return Decimal(str(self.price)) * (1 + self.PRICE_WITHOUT_DISCOUNT_MULTIPLIER)

    class Meta:
        proxy = True


class Hero(models.Model, RechargeEnergyMixin):
    ABILITY_ENERGY_CONSUMPTION: int = 0

    name = models.CharField(
        max_length=100,
    )

    hero_title = models.CharField(
        max_length=100,
    )

    energy = models.PositiveIntegerField()

    @property
    def required_energy_message(self) -> str:
        return ""

    @property
    def successful_ability_usage_message(self) -> str:
        return ""

    def use_ability(self) -> str:
        if self.energy < self.ABILITY_ENERGY_CONSUMPTION:
            return self.required_energy_message

        self.energy = max(self.energy - self.ABILITY_ENERGY_CONSUMPTION, 1)

        return self.successful_ability_usage_message


class SpiderHero(Hero):
    ABILITY_ENERGY_CONSUMPTION: int = 80

    def swing_from_buildings(self) -> str:
        return self.use_ability()

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def successful_ability_usage_message(self) -> str:
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True



class FlashHero(Hero):
    ABILITY_ENERGY_CONSUMPTION: int = 65

    def run_at_super_speed(self) -> str:
        return self.use_ability()

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def successful_ability_usage_message(self) -> str:
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True


class Document(models.Model):
    # STEPS for vector fields -> The running brown dog is in a run
    # STEP 1 tokenization -> [The, running, brown, dog, is, in, a, run]
    # STEP 2 remove stop words -> [running, brown, dog, run]
    # STEP 3 create lexems -> [run, brown, dog] -> [run: 2, 8; brown: 3; dog: 4]
    # SELECT to_tsvector('The running brown dog is in a run') @@ plainto_tsquery('runs');
    title = models.CharField(
        max_length=200,
    )

    content = models.TextField()

    search_vector = SearchVectorField(
        null=True,
        db_index=True,
    )

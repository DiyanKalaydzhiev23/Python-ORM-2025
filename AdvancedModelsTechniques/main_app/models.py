from decimal import Decimal

from django.contrib.postgres.search import SearchVectorField
from django.core.validators import MinValueValidator, EmailValidator, RegexValidator, MinLengthValidator
from django.db import models

from main_app.mixins import RechargeEnergyMixin
from main_app.validators import NameValidator, PhoneNumberValidator


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            NameValidator(message="Name can only contain letters and spaces"),
        ]
    )
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, message="Age must be greater than or equal to 18"),
        ]
    )
    email = models.EmailField(
        error_messages={'invalid': "Enter a valid email address"},
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            # RegexValidator(regex=r'^+359\d{9}$', message="Phone number must start with '+359' followed by 9 digits"),
            PhoneNumberValidator(message="Phone number must start with '+359' followed by 9 digits")
        ],
    )
    website_url = models.URLField(
        error_messages={"invalid": "Enter a valid URL"},
    )


class BaseMedia(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

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


class Book(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"

    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(5, message="Author must be at least 5 characters long"),
        ]
    )
    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(6, message="ISBN must be at least 6 characters long"),
        ]
    )


class Movie(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"

    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(8, message="Director must be at least 8 characters long"),
        ]
    )


class Music(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"

    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(9, message="Artist must be at least 9 characters long"),
        ]
    )


class Product(models.Model):
    TAX_PERCENT: Decimal = Decimal('0.08')
    SHIPPING_MULTIPLIER: Decimal = Decimal('2.00')

    name = models.CharField(
        max_length=100,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def calculate_tax(self) -> Decimal:
        return self.price * self.TAX_PERCENT

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return weight * self.SHIPPING_MULTIPLIER

    def format_product_name(self) -> str:
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    PRICE_INCREASE_PERCENT: Decimal = Decimal('0.20')
    TAX_PERCENT: Decimal = Decimal('0.05')
    SHIPPING_MULTIPLIER: Decimal = Decimal('1.50')

    class Meta:
        proxy = True

    def calculate_price_without_discount(self) -> Decimal:
        return Decimal(str(self.price)) * (1 + self.PRICE_INCREASE_PERCENT)

    def format_product_name(self) -> str:
        return f"Discounted Product: {self.name}"


class Hero(models.Model, RechargeEnergyMixin):
    ABILITY_ENERGY_REQUIRED: int = 0
    MIN_ENERGY: int = 1

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
    def successful_ability_use_message(self) -> str:
        return ""

    def use_ability(self):
        if self.energy < self.ABILITY_ENERGY_REQUIRED:
            return self.required_energy_message

        if self.energy - self.ABILITY_ENERGY_REQUIRED > 0:
            self.energy -= self.ABILITY_ENERGY_REQUIRED
        else:
            self.energy = self.MIN_ENERGY

        self.save()

        return self.successful_ability_use_message



class SpiderHero(Hero):
    ABILITY_ENERGY_REQUIRED: int = 80

    class Meta:
        proxy = True

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def successful_ability_use_message(self) -> str:
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    def swing_from_buildings(self) -> str:
        return self.use_ability()


class FlashHero(Hero):
    ABILITY_ENERGY_REQUIRED: int = 65

    class Meta:
        proxy = True

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def successful_ability_use_message(self) -> str:
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    def run_at_super_speed(self) -> str:
        return self.use_ability()



class Document(models.Model):
    # STEPS for vector fields in postgres
    # STEP 1 tokenization -> split text to words -> "The running brown dog is in a run" -> [The, running, ...]
    # STEP 2 Remove repetions -> [The, running, ...] -> [running, brown, dog, run]
    # STEP 3 Create lexems -> [run: 2; 8, brown: 3, dog: 4]
    # Example select to_tsvector('The running brown') @@ plainto_tsquery('runs'); -> true
    # Example select to_tsvector('The brown') @@ plainto_tsquery('runs'); -> false
    # plainto_tsquery('runs') -> 'run'
    # to_tsvector('The running brown') -> ['run': 2, 'brown: 3]

    title = models.CharField(
        max_length=200,
    )
    content = models.TextField()
    search_vector = SearchVectorField(
        null=True,
        db_index=True,
    )

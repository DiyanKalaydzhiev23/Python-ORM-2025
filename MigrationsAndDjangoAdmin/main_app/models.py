from django.db import models


class Shoe(models.Model):
    brand = models.CharField(
        max_length=25,
    )

    size = models.PositiveIntegerField()


class UniqueBrands(models.Model):
    brand = models.CharField(
        max_length=25,
        unique=True,
    )


class EventRegistration(models.Model):
    event_name = models.CharField(
        max_length=60,
    )

    participant_name = models.CharField(
        max_length=50,
    )

    registration_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.participant_name} - {self.event_name}"

class Movie(models.Model):
    title = models.CharField(
        max_length=100,
    )
    director = models.CharField(
        max_length=100,
    )
    release_year = models.PositiveIntegerField()

    genre = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f'Movie "{self.title}" by {self.director}'

class Student(models.Model):
    first_name = models.CharField(
        max_length=50,
    )
    last_name = models.CharField(
        max_length=50,
    )
    age = models.PositiveIntegerField()
    grade = models.CharField(
        max_length=10,
    )
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Supplier(models.Model):
    name = models.CharField(
        max_length=100,
    )

    contact_person = models.CharField(
        max_length=50,
    )

    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
    )

    address = models.TextField()

    def __str__(self) -> str:
        return f"{self.name} - {self.phone}"


class Course(models.Model):
    title = models.CharField(
        max_length=90,
    )

    lecturer = models.CharField(
        max_length=90,
    )

    description = models.CharField(
        max_length=200,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    start_date = models.DateField(
        auto_now_add=True,
    )

    is_published = models.BooleanField(
        default=True,
    )

    def __str__(self) -> str:
        return f"{self.title} - {self.lecturer}"


class Person(models.Model):
    name = models.CharField(
        max_length=40,
    )

    age = models.PositiveIntegerField()

    age_group = models.CharField(
        max_length=20,
        default='No age group',
    )

    def __str__(self) -> str:
        return f"Name: {self.name}"


class Item(models.Model):
    name = models.CharField(
        max_length=100,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    rarity = models.CharField(
        max_length=20,
        default="No rarity",
    )


class Smartphone(models.Model):
    brand = models.CharField(
        max_length=100,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    category = models.CharField(
        max_length=20,
        default="No category",
    )


class OrderStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    COMPLETED = "Completed", "Completed"
    CANCELLED = "Cancelled", "Cancelled"


class Order(models.Model):
    product_name = models.CharField(
        max_length=30,
    )
    customer_name = models.CharField(
        max_length=100,
    )
    order_date = models.DateField()
    status = models.CharField(
        max_length=30,
        choices=OrderStatus.choices,
    )
    amount = models.PositiveIntegerField(
        default=1,
    )
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    warranty = models.CharField(
        max_length=100,
        default="No warranty",
    )
    delivery = models.DateField(
        null=True,
        blank=True,
    )
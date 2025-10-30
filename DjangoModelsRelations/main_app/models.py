from datetime import timedelta

from django.db import models


class Author(models.Model):
    name = models.CharField(
        max_length=40,
    )


class Book(models.Model):
    """
    CREATE TABLE book(
        id SERIAL PRIMARY KEY,
        title VARCHAR(40),
        price DECIMAL(5, 2),
        author INT FOREIGN KEY(author) REFERENCES author(id)
    );
    """
    title = models.CharField(
        max_length=40,
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
    )


class Song(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
    )


class Artist(models.Model):
    name = models.CharField(
        max_length=100,
    )

    songs = models.ManyToManyField(
        to=Song,
        related_name="artists",
    )


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )


class Review(models.Model):
    description = models.TextField(
        max_length=200,
    )
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )


class Driver(models.Model):
    first_name = models.CharField(
        max_length=50,
    )

    last_name = models.CharField(
        max_length=50,
    )


class DrivingLicense(models.Model):
    license_number = models.CharField(
        max_length=10,
        unique=True,
    )

    issue_date = models.DateField()

    driver = models.OneToOneField(
        to=Driver,
        on_delete=models.CASCADE,
        related_name="license",
    )

    @property
    def expiration_date(self):
        return self.issue_date + timedelta(days=365)

    def __str__(self) -> str:
        return f"License with number: {self.license_number} expires on {self.expiration_date}!"


class Owner(models.Model):
    name = models.CharField(
        max_length=50,
    )


class Car(models.Model):
    model = models.CharField(
        max_length=50,
    )

    year = models.PositiveIntegerField()

    owner = models.ForeignKey(
        to=Owner,
        on_delete=models.CASCADE,
        related_name='cars',
        blank=True,
        null=True,
    )


class Registration(models.Model):
    registration_number = models.CharField(
        max_length=10,
        unique=True,
    )

    registration_date = models.DateField(
        blank=True,
        null=True,
    )

    car = models.OneToOneField(
        to=Car,
        on_delete=models.CASCADE,
        related_name="registration",
        blank=True,
        null=True,
    )

from datetime import timedelta

from django.db import models


class Author(models.Model):
    """
    CREATE TABLE main_app_author (
        id INT PRIMARY KEY,
        name VARCHAR(40)
    );
    """
    name = models.CharField(
        max_length=40,
    )


class Book(models.Model):
    """
    CREATE TABLE main_app_book (
        id INT PRIMARY KEY,
        title VARCHAR(40),
        price DECIMAL(5, 2),
        author INT,

        FOREIGN KEY (author)
        REFERENCES main_app_author(id)
        ON DELETE CASCADE
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
        Author,
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
        unique=True,
    )
    songs = models.ManyToManyField(
        Song,
        related_name="artists",
    )


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )


class Review(models.Model):
    description = models.CharField(
        max_length=200,
    )
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"  # in order not to write review_set
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
    driver = models.OneToOneField(  # driver_id will be unique
        Driver,
        on_delete=models.CASCADE,
        related_name="license",
    )

    def __str__(self):
        expiration_date = self.issue_date + timedelta(days=365)
        return f"License with number: {self.license_number} expires on {expiration_date}!"


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
        Owner,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="cars"
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
        Car,
        on_delete=models.CASCADE,
        related_name="registration",
        blank=True,
        null=True,
    )

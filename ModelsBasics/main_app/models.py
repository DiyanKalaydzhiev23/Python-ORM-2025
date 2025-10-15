from django.db import models

from main_app.choices import GenreChoices


class Person(models.Model):
    name = models.CharField(
        max_length=30,
    )  # VARCHAR

    age = models.PositiveIntegerField()  # INTEGER + CHECK > 0


class Blog(models.Model):
    post = models.TextField()  # TEXT

    author = models.CharField(
        max_length=35,
    )


class WeatherForecast(models.Model):
    date = models.DateField()  # DATE
    temperature = models.FloatField()  # FLOAT
    humidity = models.FloatField()
    precipitation = models.FloatField()


class Recipe(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField()

    ingredients = models.TextField()

    cook_time = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )  # TIMESTAMP


class Product(models.Model):
    name = models.CharField(
        max_length=70,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class UserProfile(models.Model):
    username = models.CharField(
        max_length=65,
        unique=True,
    )

    first_name = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        default="students@softuni.bg",
    )

    bio = models.TextField(
        max_length=120,
    )

    profile_image_url = models.URLField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Exercise(models.Model):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    difficulty_level = models.CharField(
        max_length=20,
    )

    duration_minutes = models.PositiveIntegerField()

    equipment = models.CharField(
        max_length=90,
    )

    video_url = models.URLField(
        blank=True,
        null=True,
    )

    calories_burned = models.PositiveIntegerField(
        default=1,
    )

    is_favorite = models.BooleanField(
        default=False,
    )


class Book(models.Model):
    # GENRE_CHOICES = (
    #     ("Fiction", "Fiction"),
    #     ("Non-Fiction", "Non-Fiction"),
    #     ...
    # )

    title = models.CharField(
        max_length=30
    )
    author = models.CharField(
        max_length=100
    )
    genre = models.CharField(
        max_length=20,
        choices=GenreChoices.choices
    )
    publication_date = models.DateField(
        auto_now_add=True,
        editable=False
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    is_available = models.BooleanField(
        default=True
    )
    rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title









from django.db import models


class GenreChoices(models.TextChoices):
    FICTION = "Fiction", "Fiction"
    NON_FICTION = "Non-Fiction", "Non-Fiction"
    SCIENCE_FICTION = "Science Fiction", "Science Fiction"
    HORROR = "Horror", "Horror"

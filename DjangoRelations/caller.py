import os
from datetime import datetime, timedelta
from itertools import product

import django
from django.db.models import QuerySet, Avg
from django.template.defaultfilters import title

from helpers import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from main_app.models import Author, Book, Artist, Song, Review, Product, DrivingLicense, Driver, Owner, Car, \
    Registration


def show_all_authors_with_their_books() -> str:
    """
    SELECT * FROM authors;
    SELECT * FROM book WHERE author_id IN (SELECT author_id FROM authors)
    """

    # prefetch is better
    # authors_books = Author.objects.prefetch_related("book_set").order_by("id")

    authors = Author.objects.all().order_by("id")
    authors_with_books = []

    for author in authors:
        books = Book.objects.filter(author=author)

        if not books:
            continue

        titles = ', '.join(b.title for b in books)
        authors_with_books.append(
            f"{author.name} has written - {titles}!"
        )

    return "\n".join(authors_with_books)


def delete_all_authors_without_books() -> None:
    """
    SELECT * FROM "main_app_author"
    LEFT OUTER JOIN "main_app_book"
    ON ("main_app_author"."id" = "main_app_book"."author_id")
    WHERE "main_app_book"."id" IS NULL;

    -- This is done because of DELETE CASCADE
    DELETE FROM "main_app_book"
    WHERE "main_app_book"."author_id" IN (list_of_ids);

    DELETE FROM "main_app_author"
    WHERE "main_app_author"."id" IN (list_of_ids);
    """
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    """
    INSERT INTO "main_app_artist_songs" ("artist_id", "song_id") VALUES (1, 1);
    """

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    artist = Artist.objects.get(name=artist_name)
    return artist.songs.all().order_by("-id")


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    """
    DELETE FROM "main_app_artist_songs" WHERE ("main_app_artist_songs"."artist_id" = 1 AND "main_app_artist_songs"."song_id" IN (1))
    """

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    """
    SELECT
        "id",
        "name",
        AVG("main_app_review"."rating") AS "avg_review_score"
    FROM
        "main_app_product"
    LEFT OUTER JOIN
        "main_app_review"
    ON
        ("id" = "product_id")
    WHERE
        "name" = 'Product 3'
    GROUP BY
        "id", "name"
    """

    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()

    average_rating = sum(r.rating for r in reviews) / len(reviews)

    # product = Product.objects.annotate(
    #     avg_review_score=Avg('reviews__rating')
    # ).get(name=product_name)

    return average_rating


def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews() -> QuerySet[Product]:
    """
    SELECT
        *
    FROM
        products AS p
    LEFT JOIN
        reviews AS r
    ON
       p.id = r.product_id
    WHERE
       r.id IS NULL
    ORDER BY
        name DESC;
    """
    return Product.objects.filter(reviews__isnull=True).order_by("-name")


def delete_products_without_reviews() -> None:
    Product.objects.filter(reviews__isnull=True).delete()



def calculate_licenses_expiration_dates() -> str:
    licenses = DrivingLicense.objects.all().order_by("-license_number")
    return "\n".join(str(l) for l in licenses)


# 01.01.2026 -> issue_date < 01.01.2025 -> invalid
def get_drivers_with_expired_licenses(due_date: datetime.date) -> QuerySet[Driver]:
    """
    SELECT
        *
    FROM
        "main_app_driver"
    INNER JOIN
        "main_app_drivinglicense"
    ON
        ("main_app_driver"."id" = "main_app_drivinglicense"."driver_id")
    WHERE
        "main_app_drivinglicense"."issue_date" < '2025-01-01'
    """
    latest_possible_issue_date = due_date - timedelta(days=365)

    drivers_with_expired_license = Driver.objects.filter(
        license__issue_date__gt=latest_possible_issue_date  # should be __lt
    )

    return drivers_with_expired_license


def register_car_by_owner(owner: Owner) -> str:
    car = Car.objects.filter(registration__isnull=True).first()
    registration = Registration.objects.filter(car__isnull=True).first()

    car.owner = owner
    car.registration = registration

    car.save()

    registration.registration_date = datetime.today()
    registration.car = car

    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

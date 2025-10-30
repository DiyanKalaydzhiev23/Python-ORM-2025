import os
from datetime import date, timedelta, datetime

import django
from django.db.models import QuerySet, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Car, \
    Registration

"""
SELECT * FROM authors;
SELECT * FROM book WHERE author_id = <id>; -- for every author
"""
def show_all_authors_with_their_books() -> str:
    authors = Author.objects.all()  # SELECT * FROM authors;
    authors_with_books = []

    for author in authors:
        books = author.book_set.all()  # SELECT * FROM book WHERE author_id = <id>;

        if not books:
            continue

        titles = ', '.join(b.title for b in books)
        authors_with_books.append(
            f"{author.name} has written - {titles}!",
        )

    return '\n'.join(authors_with_books)

"""
SELECT * FROM "main_app_author" 
LEFT JOIN "main_app_book" 
ON ("main_app_author"."id" = "main_app_book"."author_id") 
WHERE "main_app_book"."id" IS NULL
"""
def delete_all_authors_without_books() -> None:
    Author.objects.filter(book__isnull=True).delete()


"""
SELECT * FROM artist WHERE name = <artist_name>;
SELECT * FROM song WHERE title = <song_title>;

INSERT INTO artist_songs...;
"""
def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    return Artist.objects.get(
        name=artist_name
    ).songs.order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)

"""
-- Solution 2 SQL
SELECT
    id,
    name,
    AVG(review.rating)
FROM 
    product
LEFT JOIN 
    reviews
ON
    ...
WHERE
    product.name = <name>
GROUP BY
    id,
    product.name;
"""
def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()

    avg_score = sum(r.rating for r in reviews) / len(reviews)

    return avg_score

    # Option 2
    # return Product.objects.annotate(
    #     avg_review_score=Avg('reviews__rating'),
    # ).get(name=product_name).avg_review_score


"""
SELECT * reviews WHERE rating >= <threshold>;
"""
def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews() -> QuerySet[Product]:
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews() -> None:
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates() -> str:
    licenses = DrivingLicense.objects.order_by('-license_number')
    return "\n".join(str(l) for l in licenses)


def get_drivers_with_expired_licenses(due_date: date) -> QuerySet[Driver]:
    # Option 1
    # licenses = DrivingLicense.objects.all()
    # expired_licenses_drivers = []
    #
    # for l in licenses:
    #     if l.expiration_date > due_date:
    #         expired_licenses_drivers.append(l.driver)
    #
    # return expired_licenses_drivers

    # Option 2
    return Driver.objects.filter(
        license__issue_date__lt=due_date - timedelta(365),
    )


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

from django.db import models
from django.db.models import Count, Avg

from main_app.querysets import RealEstateListingQuerySet, VideoGameQuerySet


class RealEstateListingManager(models.Manager.from_queryset(RealEstateListingQuerySet)):
    def popular_locations(self) -> dict:
        """
        SELECT
            location,
            COUNT(location) AS location_count
        FROM
            real_estate_listing
        GROUP BY
            location
        ORDER BY
            location_count DESC,
            location ASC
        LIMIT 2;
        """
        return self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]


class VideoGameManager(models.Manager.from_queryset(VideoGameQuerySet)):
    def highest_rated_game(self) -> 'VideoGame':
        """
        SELECT
            *
        FROM
            video_game
        ORDER BY
            rating DESC
        LIMIT 1;
        """
        return self.order_by('-rating').first()

    def lowest_rated_game(self) -> 'VideoGame':
        return self.order_by('rating').first()

    def average_rating(self) -> str:
        """
        SELECT
            AVG(rating) AS average_rating
        FROM
            video_game
        """
        average_rating = self.aggregate(
            average_rating=Avg('rating')
        )['average_rating']  # {'average_rating': 10}
        return f"{average_rating:.1f}"



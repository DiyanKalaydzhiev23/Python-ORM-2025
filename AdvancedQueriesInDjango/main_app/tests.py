from django.core.exceptions import ValidationError
from django.test import TestCase

from main_app.models import VideoGame


class VideoGameModelTests(TestCase):
    def test_invalid_rating(self):
        """
        Test that a ValidationError is raised when creating a VideoGame instance with an invalid rating.
        """
        # Test for an invalid rating (outside the range).
        with self.assertRaises(ValidationError) as context:
            VideoGame(title='Invalid Game', genre='Action', release_year=2021, rating=-0.1).full_clean()

        # Check the error message
        expected_error_message = 'The rating must be between 0.0 and 10.0'
        self.assertTrue(expected_error_message in str(context.exception))

        with self.assertRaises(ValidationError) as context:
            VideoGame(title='Invalid Game', genre='Action', release_year=2021, rating=10.6).full_clean()

        # Check the error message
        expected_error_message = 'The rating must be between 0.0 and 10.0'
        self.assertTrue(expected_error_message in str(context.exception))
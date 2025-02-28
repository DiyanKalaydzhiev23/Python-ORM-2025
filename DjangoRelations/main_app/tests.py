from datetime import date, timedelta

from django.test import TestCase

from main_app.models import Driver, DrivingLicense


def get_drivers_with_expired_licenses(due_date):
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
        license__issue_date__lt=latest_possible_issue_date
    )

    return drivers_with_expired_license


class LicenseTestCase(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(first_name='John', last_name='Doe')
        self.driver2 = Driver.objects.create(first_name='Jane', last_name='Smith')

        issue_date1 = date(2022, 1, 1)
        issue_date2 = date(2021, 1, 1)

        self.license1 = DrivingLicense.objects.create(
            license_number='DL001', issue_date=issue_date1, driver=self.driver1
        )

        self.license2 = DrivingLicense.objects.create(
            license_number='DL002', issue_date=issue_date2, driver=self.driver2
        )

    def test_get_drivers_with_expired_licenses(self):
        """
        Test the get_drivers_with_expired_licenses function to ensure it correctly identifies drivers with expired licenses based on a given date.
        """
        given_date = date(2022, 12, 31)
        drivers_with_expired_licenses = get_drivers_with_expired_licenses(given_date)
        self.assertEqual(len(drivers_with_expired_licenses), 1)
        self.assertIn(self.driver2, drivers_with_expired_licenses)
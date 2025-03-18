from django.db.models import manager, QuerySet, Count


class ProfileManager(manager.Manager):
    def get_regular_customers(self) -> QuerySet:
        return self.annotate(
            count_orders=Count('order'),
        ).filter(
            count_orders__gt=2
        ).order_by(
            '-count_orders',
        )

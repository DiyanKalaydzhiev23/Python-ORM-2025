import os
from typing import Optional

import django
from django.db.models import Q, Count, F, Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from helpers import populate_model_with_data
from main_app.models import Profile, Product, Order


def populate_db() -> None:
    populate_model_with_data(Profile)
    populate_model_with_data(Product)
    populate_model_with_data(Order)


def get_profiles(search_string: Optional[str]=None) -> str:
    if not search_string:
        return ""

    profiles_match = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by("full_name")
    # Todo: for optimization add prefetch

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_set.count()}"
        for p in profiles_match
    )


def get_loyal_profiles() -> str:
    return "\n".join(
        f"Profile: {p.full_name}, orders: {p.count_orders}"
        for p in Profile.objects.get_regular_customers()
    )


def get_last_sold_products() -> str:
    last_order = Order.objects.last()

    if not last_order:
        return ""

    return f"Last sold products: {', '.join(p.name for p in last_order.products.all())}"


def get_top_products() -> str:
    top_products = Product.objects.annotate(
        orders_count=Count('order'),
    ).filter(
        orders_count__gt=0,
    ).order_by(
        '-orders_count',
        'name'
    )[:5]

    if not top_products.exists():
        return ""

    return "Top products:\n" + "\n".join(
        f"{p.name}, sold {p.orders_count} times"
        for p in top_products
    )


def apply_discounts() -> str:
    updated_records_count = Order.objects.annotate(
        products_count=Count('products'),
    ).filter(
        products_count__gt=2,
        is_completed=False,
    ).update(
        total_price=F('total_price') * 0.90,
    )

    return f"Discount applied to {updated_records_count} orders."


def complete_order() -> str:
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ""

    order.is_completed = True
    Product.objects.filter(order=order).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
        )
    )

    order.save()

    return "Order has been completed!"

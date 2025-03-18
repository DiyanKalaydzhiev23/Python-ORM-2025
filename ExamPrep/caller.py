import os
import django
from django.db.models import Q, Count, F, Case, When, Value

from helpers import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order


def populate_db() -> None:
    populate_model_with_data(Profile, num_records=2)
    populate_model_with_data(Product, num_records=2)
    populate_model_with_data(Order, num_records=2)



def get_profiles(search_string: str=None) -> str:

    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
            |
        Q(email__icontains=search_string)
    ).order_by('full_name')

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_set.count()}"
        for p in profiles
    )


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    return "\n".join(
        f"Profile: {p.full_name}, orders: {p.count_orders}"
        for p in profiles
    )


def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ""

    products_names = [p.name for p in last_order.products.all()]

    return f"Last sold products: {', '.join(products_names)}"


def get_top_products() -> str:
    top_products = Product.objects.annotate(
        orders_count=Count('order'),
    ).filter(
        orders_count__gt=0,
    ).order_by(
        '-orders_count',
        'name',
    )[:5]

    if not top_products.exists():
        return ""

    return "Top products:\n" + "\n".join(
        f"{p.name}, sold {p.orders_count} times"
        for p in top_products
    )


def apply_discounts() -> str:
    updated_orders_count: int = Order.objects.annotate(
        products_count=Count('products'),
    ).filter(
        products_count__gt=2,
        is_completed=False,
    ).update(
        total_price=F('total_price') * 0.90,
    )

    return f"Discount applied to {updated_orders_count} orders."


def complete_order() -> str:
    order = Order.objects.filter(
        is_completed=False,
    ).order_by(
        'creation_date'
    ).first()

    if order is None:
        return ""

    # Not that optimized solution
    # for p in order.products.all():
    #     p.is_stock -= 1
    #
    #     if p.stock == 0:
    #         p.is_available = False
    #
    #     p.save()

    Product.objects.filter(order=order).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available')
        )
    )

    order.is_completed = True
    order.save()

    return "Order has been completed!"

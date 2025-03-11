import os
from decimal import Decimal

import django
from django.core.exceptions import ValidationError

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Customer

customer = Customer(
    name="Svetlin Nakov1",
    age=1,
    email="nakov@example",
    phone_number="+35912345678",
    website_url="htsatps://nakov.com/"
)

try:
    customer.full_clean()
    customer.save()

except ValidationError as e:
    print('\n'.join(e.messages))

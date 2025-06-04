from decimal import Decimal

import factory
from order.models import Order


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    status = "pending"
    total_price = Decimal("0.00")

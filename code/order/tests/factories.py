from decimal import Decimal

import factory
from django.contrib.auth.models import User
from event.tests.factories import EventFactory
from order.models import Order, OrderStatus


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")


class OrderStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderStatus

    status = factory.Sequence(lambda n: f"Status {n}")


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventFactory)
    total_price = Decimal("0.00")
    status = factory.SubFactory(OrderStatusFactory)
    establishment_fee = Decimal("5.00")
    payment_status = "pending"

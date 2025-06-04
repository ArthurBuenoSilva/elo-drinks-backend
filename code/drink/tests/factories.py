from decimal import Decimal

import factory
from drink.models import Category, Drink, OrderDrink
from order.tests.factories import OrderFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class DrinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Drink

    name = factory.Sequence(lambda n: f"Drink {n}")
    description = "Some description"
    ingredients = "Water, Sugar"
    is_open_letter = False
    price = Decimal("10.00")
    available = True
    category = factory.SubFactory(CategoryFactory)


class OrderDrinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderDrink

    order = factory.SubFactory(OrderFactory)
    drink = factory.SubFactory(DrinkFactory)
    quantity = 2

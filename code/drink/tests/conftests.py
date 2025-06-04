import pytest

from .factories import CategoryFactory, DrinkFactory, OrderDrinkFactory

pytest_factoryboy = pytest.importorskip("pytest_factoryboy")

pytest_factoryboy.register(CategoryFactory)
pytest_factoryboy.register(DrinkFactory)
pytest_factoryboy.register(OrderDrinkFactory)

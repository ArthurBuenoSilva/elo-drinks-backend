import pytest

from .factories import OrderFactory, OrderStatusFactory

pytest_factoryboy = pytest.importorskip("pytest_factoryboy")

pytest_factoryboy.register(OrderFactory)
pytest_factoryboy.register(OrderStatusFactory)

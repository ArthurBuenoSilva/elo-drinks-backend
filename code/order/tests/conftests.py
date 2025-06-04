import pytest

from .factories import OrderFactory

pytest_factoryboy = pytest.importorskip("pytest_factoryboy")

pytest_factoryboy.register(OrderFactory)

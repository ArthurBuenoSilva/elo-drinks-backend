import pytest

from .factories import EventFactory

pytest_factoryboy = pytest.importorskip("pytest_factoryboy")

pytest_factoryboy.register(EventFactory)

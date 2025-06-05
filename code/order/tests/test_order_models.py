from decimal import Decimal

from django.contrib.auth.models import User
from event.tests.factories import EventFactory

from .factories import OrderFactory, OrderStatusFactory


def test_order_status():
    mock_status = OrderStatusFactory.build(status="In Progress")
    assert mock_status.status == "In Progress"


def test_order():
    mock_user = User(username="testuser")
    mock_event = EventFactory.build(name="Music Festival")
    mock_status = OrderStatusFactory.build(status="Pending")

    mock_order = OrderFactory.build(
        user=mock_user,
        event=mock_event,
        total_price=Decimal("50.00"),
        status=mock_status,
        establishment_fee=Decimal("5.00"),
        payment_status="pending",
    )

    assert mock_order.user == mock_user
    assert mock_order.event == mock_event
    assert mock_order.total_price == Decimal("50.00")
    assert mock_order.status == mock_status
    assert mock_order.establishment_fee == Decimal("5.00")
    assert mock_order.payment_status == "pending"

import pytest
from django.contrib.auth.models import User
from event.models import Event
from order.models import Order, OrderStatus
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_order_status():
    client = APIClient()

    payload = {
        "status": "Pending",
    }

    response = client.post("/api/order/statuses/", payload, format="json")

    assert response.status_code == 201
    status_id = response.data["id"]

    status = OrderStatus.objects.get(pk=status_id)
    assert status.status == "Pending"


@pytest.mark.django_db
def test_create_order():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="password")
    event = Event.objects.create(
        name="Tech Conference",
        date="2025-12-25T18:00:00Z",
        location="São Paulo",
        description="A conference about technology",
        people_quantity=500,
    )
    status = OrderStatus.objects.create(status="Pending")

    payload = {
        "user": user.id,
        "event": event.id,
        "status": status.id,
        "establishment_fee": "5.00",
        "payment_status": "pending",
    }

    response = client.post("/api/order/orders/", payload, format="json")

    assert response.status_code == 201
    order_id = response.data["id"]

    order = Order.objects.get(pk=order_id)
    assert order.user == user
    assert order.event == event
    assert order.status == status
    assert order.establishment_fee == 5
    assert order.payment_status == "pending"

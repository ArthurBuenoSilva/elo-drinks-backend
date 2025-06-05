import pytest
from django.contrib.auth.models import User
from drink.models import Category, Drink
from event.models import Event
from order.models import Order, OrderStatus
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_category():
    client = APIClient()

    payload = {
        "name": "Soft Drinks",
    }

    response = client.post("/api/drink/categories/", payload, format="json")

    assert response.status_code == 201
    category_id = response.data["id"]

    category = Category.objects.get(pk=category_id)
    assert category.name == "Soft Drinks"


@pytest.mark.django_db
def test_create_drink():
    client = APIClient()

    category = Category.objects.create(name="Cocktails")

    payload = {
        "name": "Mojito",
        "description": "Refreshing mint cocktail",
        "ingredients": "Mint, Sugar, Lime, Rum, Soda",
        "is_open_letter": False,
        "price": "15.00",
        "available": True,
        "category": category.id,
    }

    response = client.post("/api/drink/drinks/", payload, format="json")

    assert response.status_code == 201
    drink_id = response.data["id"]

    drink = Drink.objects.get(pk=drink_id)
    assert drink.name == "Mojito"
    assert drink.description == "Refreshing mint cocktail"
    assert drink.ingredients == "Mint, Sugar, Lime, Rum, Soda"
    assert drink.price == 15
    assert drink.available is True
    assert drink.category == category


@pytest.mark.django_db
def test_create_order_drink():
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="password")
    event = Event.objects.create(
        name="Music Fest",
        date="2025-12-31T18:00:00Z",
        location="Rio",
        description="New Year Festival",
        people_quantity=1000,
    )
    status = OrderStatus.objects.create(status="Pending")
    order = Order.objects.create(
        user=user, event=event, total_price=0, status=status, establishment_fee=5, payment_status="pending"
    )
    category = Category.objects.create(name="Beers")
    drink = Drink.objects.create(
        name="IPA Beer",
        description="Craft beer",
        ingredients="Water, Malt, Hops, Yeast",
        is_open_letter=False,
        price=12,
        available=True,
        category=category,
    )

    payload = {"order": order.id, "drink": drink.id, "quantity": 2}

    response = client.post("/api/drink/order-drinks/", payload, format="json")

    assert response.status_code == 201
    assert response.data["quantity"] == 2
    assert float(response.data["total_price"]) == 24.0

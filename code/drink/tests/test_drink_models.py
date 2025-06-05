from decimal import Decimal

from drink.models import OrderDrink

from .factories import CategoryFactory, DrinkFactory


def test_category():
    mock_category = CategoryFactory.build(name="test_category")
    assert mock_category.name == "test_category"


def test_drink():
    mock_category = CategoryFactory.build(name="Juice")

    mock_drink = DrinkFactory.build(
        name="Orange Juice",
        description="Refreshing Orange Juice",
        ingredients="Orange and Water",
        price=Decimal("5"),
        category=mock_category,
    )
    assert mock_drink.name == "Orange Juice"
    assert mock_drink.description == "Refreshing Orange Juice"
    assert mock_drink.ingredients == "Orange and Water"
    assert mock_drink.price == Decimal("5")
    assert mock_drink.category == mock_category


def test_calculate_total_price():
    mock_drink = DrinkFactory.build(price=Decimal("10.00"))

    order_drink = OrderDrink(quantity=3)
    order_drink.drink = mock_drink

    result = order_drink.calculate_total_price()

    assert result == Decimal("30.00")

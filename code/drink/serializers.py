from rest_framework import serializers

from .models import Category, Drink, OrderDrink


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = [
            "id",
            "name",
            "description",
            "ingredients",
            "is_open_letter",
            "price",
            "available",
            "category",
            "created_at",
        ]


class OrderDrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDrink
        fields = ["id", "order_id", "drink", "quantity", "total_price"]

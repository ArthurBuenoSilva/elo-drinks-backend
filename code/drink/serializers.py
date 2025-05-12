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
        fields = ["id", "order", "drink", "quantity", "total_price"]
        read_only_fields = ["total_price"]

    def create(self, validated_data):
        instance = super().create(validated_data)
        self._recalculate_order_total(instance.order)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self._recalculate_order_total(instance.order)
        return instance

    @staticmethod
    def _recalculate_order_total(order):
        drinks_total = sum(od.total_price for od in order.orderdrink_set.all())
        order.total_price = drinks_total
        order.save()

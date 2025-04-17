from rest_framework import serializers
from .models import Order, OrderStatus


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['id', 'status']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'event', 'total_price', 'status', 'establishment_fee', 'payment_status', 'created_at']

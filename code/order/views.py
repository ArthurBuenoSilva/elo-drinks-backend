from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import OrderFilter, OrderStatusFilter
from .models import Order, OrderStatus
from .serializers import OrderSerializer, OrderStatusSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter


class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderStatusFilter

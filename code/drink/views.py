from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import CategoryFilter, DrinkFilter, OrderDrinkFilter
from .models import Category, Drink, OrderDrink
from .serializers import CategorySerializer, DrinkSerializer, OrderDrinkSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DrinkFilter


class OrderDrinkViewSet(viewsets.ModelViewSet):
    queryset = OrderDrink.objects.all()
    serializer_class = OrderDrinkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderDrinkFilter

    def perform_destroy(self, instance):
        order = instance.order
        instance.delete()
        drinks_total = sum(od.total_price for od in order.orderdrink_set.all())
        order.total_price = drinks_total + order.establishment_fee
        order.save()

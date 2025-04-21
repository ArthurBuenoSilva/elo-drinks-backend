from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, DrinkViewSet, OrderDrinkViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"drinks", DrinkViewSet, basename="drink")
router.register(r"order-drinks", OrderDrinkViewSet, basename="orderdrink")

urlpatterns = [
    path("", include(router.urls)),
]

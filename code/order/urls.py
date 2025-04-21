from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderStatusViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"statuses", OrderStatusViewSet, basename="orderstatus")

urlpatterns = [
    path("", include(router.urls)),
]

import django_filters

from .models import Order, OrderStatus


class OrderStatusFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = OrderStatus
        fields = ["status"]


class OrderFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name="user__id")
    event = django_filters.NumberFilter(field_name="event__id")
    status = django_filters.NumberFilter(field_name="status__id")
    payment_status = django_filters.ChoiceFilter(choices=Order.PAYMENT_STATUS_CHOICES)
    price_min = django_filters.NumberFilter(field_name="total_price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="total_price", lookup_expr="lte")

    class Meta:
        model = Order
        fields = ["user", "event", "status", "payment_status", "price_min", "price_max"]

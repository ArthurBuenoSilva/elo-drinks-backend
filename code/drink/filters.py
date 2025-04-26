import django_filters

from .models import Category, Drink, OrderDrink


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["name"]


class DrinkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    ingredient = django_filters.CharFilter(method="filter_by_ingredient")
    category = django_filters.NumberFilter(field_name="category__id")
    is_open_letter = django_filters.BooleanFilter()
    available = django_filters.BooleanFilter()

    class Meta:
        model = Drink
        fields = ["name", "ingredient", "category", "is_open_letter", "available"]

    @staticmethod
    def filter_by_ingredient(queryset, name):
        return queryset.filter(ingredients__icontains=name)


class OrderDrinkFilter(django_filters.FilterSet):
    order = django_filters.NumberFilter(field_name="order__id")
    drink = django_filters.NumberFilter(field_name="drink__id")
    quantity_min = django_filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = django_filters.NumberFilter(field_name="quantity", lookup_expr="lte")

    class Meta:
        model = OrderDrink
        fields = ["order", "drink", "quantity_min", "quantity_max"]

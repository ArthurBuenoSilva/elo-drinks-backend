import django_filters

from .models import Event


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(lookup_expr="icontains")
    date_after = django_filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    date_before = django_filters.DateTimeFilter(field_name="date", lookup_expr="lte")
    min_people = django_filters.NumberFilter(field_name="people_quantity", lookup_expr="gte")
    max_people = django_filters.NumberFilter(field_name="people_quantity", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ["name", "location", "date_after", "date_before", "min_people", "max_people"]

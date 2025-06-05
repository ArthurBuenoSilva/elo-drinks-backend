from datetime import datetime

import factory
from event.models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Sequence(lambda n: f"Event {n}")
    date = factory.LazyFunction(lambda: datetime(2025, 1, 1, 12, 0))
    location = "Default Location"
    description = "Default Description"
    people_quantity = 100

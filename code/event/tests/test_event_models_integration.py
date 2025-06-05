import pytest
from event.models import Event
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_event():
    client = APIClient()

    payload = {
        "name": "Tech Conference",
        "date": "2025-12-25T18:00:00Z",
        "location": "São Paulo",
        "description": "A conference about technology",
        "people_quantity": 500,
    }

    response = client.post("/api/event/events/", payload, format="json")

    assert response.status_code == 201
    event_id = response.data["id"]

    event = Event.objects.get(pk=event_id)
    assert event.name == "Tech Conference"
    assert event.location == "São Paulo"
    assert event.description == "A conference about technology"
    assert event.people_quantity == 500

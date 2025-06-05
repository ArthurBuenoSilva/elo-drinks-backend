from datetime import datetime

from .factories import EventFactory


def test_event():
    mock_event = EventFactory.build(
        name="Tech Conference",
        date=datetime(2025, 12, 25, 18, 0),
        location="São Paulo",
        description="A conference about technology",
        people_quantity=500,
    )

    assert mock_event.name == "Tech Conference"
    assert mock_event.date == datetime(2025, 12, 25, 18, 0)
    assert mock_event.location == "São Paulo"
    assert mock_event.description == "A conference about technology"
    assert mock_event.people_quantity == 500

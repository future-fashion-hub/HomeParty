from events import add_event, find_event, sort_events
from models import Event


def test_event_creation() -> None:
    event = Event(
        event_id=1,
        name="День рождения",
        event_date="2026-10-10",
        budget=18000,
    )

    assert event.id == 1
    assert event.name == "День рождения"
    assert event.date == "2026-10-10"
    assert event.budget == 18000


def test_event_str() -> None:
    event = Event(
        event_id=1,
        name="День рождения",
        event_date="2026-10-10",
        budget=18000,
    )

    assert "День рождения" in str(event)
    assert "2026-10-10" in str(event)


def test_add_event() -> None:
    events: list[Event] = []

    event = add_event(
        events,
        "День рождения",
        "2026-10-10",
        18000,
    )

    assert len(events) == 1
    assert events[0] is event


def test_find_event() -> None:
    events = [
        Event(1, "День рождения", "2026-10-10", 18000),
        Event(2, "Новый год", "2026-12-31", 25000),
    ]

    result = find_event(
        events,
        "день",
    )

    assert len(result) == 1
    assert result[0].name == "День рождения"


def test_sort_events() -> None:
    events = [
        Event(1, "Новый год", "2026-12-31", 25000),
        Event(2, "День рождения", "2026-10-10", 18000),
    ]

    result = sort_events(events)

    assert result[0].date == "2026-10-10"
    assert result[1].date == "2026-12-31"


def test_event_budget() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    assert event.is_budget_enough(15000)
    assert not event.is_budget_enough(20000)

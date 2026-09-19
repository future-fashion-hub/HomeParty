from datetime import date

from events import add_event, find_event, sort_events


def test_add_event():
    events = []

    add_event(
        events,
        "День рождения",
        date(2026, 10, 10),
        18000,
    )

    assert len(events) == 1
    assert events[0]["name"] == "День рождения"
    assert events[0]["budget"] == 18000


def test_find_event():
    events = []

    add_event(
        events,
        "День рождения",
        date(2026, 10, 10),
        18000,
    )

    result = find_event(events, "рожд")

    assert len(result) == 1
    assert result[0]["name"] == "День рождения"


def test_sort_events():
    events = []

    add_event(
        events,
        "Новый год",
        date(2026, 12, 31),
        30000,
    )

    add_event(
        events,
        "День рождения",
        date(2026, 10, 10),
        18000,
    )

    result = sort_events(events)

    assert result[0]["name"] == "День рождения"
    assert result[1]["name"] == "Новый год"

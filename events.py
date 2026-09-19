from datetime import date


def add_event(
    events: list[dict],
    name: str,
    event_date: date,
    budget: float,
) -> dict:
    """Добавить новое событие."""
    event_id = len(events) + 1

    event = {
        "id": event_id,
        "name": name,
        "date": event_date.isoformat(),
        "budget": budget,
    }

    events.append(event)
    return event


def find_event(
    events: list[dict],
    query: str,
) -> list[dict]:
    """Найти события по названию."""
    query = query.lower()

    return [
        event
        for event in events
        if query in event["name"].lower()
    ]


def get_event_info(event: dict) -> str:
    """Получить информацию о событии."""
    return (
        f"Событие: {event['name']}, "
        f"дата: {event['date']}, "
        f"бюджет: {event['budget']} руб."
    )


def sort_events(events: list[dict]) -> list[dict]:
    """Отсортировать события по дате."""
    return sorted(
        events,
        key=lambda event: event["date"],
    )

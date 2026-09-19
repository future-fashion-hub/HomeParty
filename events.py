from models import Event


def add_event(
    events: list[Event],
    name: str,
    event_date: str,
    budget: float,
) -> Event:
    """Добавить новое событие."""
    event_id = len(events) + 1

    event = Event(
        event_id=event_id,
        name=name,
        event_date=event_date,
        budget=budget,
    )

    events.append(event)
    return event


def find_event(
    events: list[Event],
    query: str,
) -> list[Event]:
    """Найти события по названию."""
    query = query.lower()

    return [
        event
        for event in events
        if query in event.name.lower()
    ]


def get_event_info(event: Event) -> str:
    """Получить информацию о событии."""
    return str(event)


def sort_events(
    events: list[Event],
) -> list[Event]:
    """Отсортировать события по дате."""
    return sorted(
        events,
        key=lambda event: event.date,
    )

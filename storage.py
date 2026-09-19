import json
from pathlib import Path
from typing import Any

from models import Event, Expense, Participant, Task


def read_json(filename: str) -> list[dict[str, Any]]:
    """Прочитать данные из JSON-файла."""
    path = Path(filename)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def write_json(
    filename: str,
    data: list[dict[str, Any]],
) -> None:
    """Сохранить данные в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )


def find_event_by_id(
    events: list[Event],
    event_id: int,
) -> Event | None:
    """Найти событие по идентификатору."""
    for event in events:
        if event.id == event_id:
            return event

    return None


def load_events(
    filename: str,
) -> list[Event]:
    """Загрузить события из JSON."""
    data = read_json(filename)
    events = []

    for item in data:
        event = Event(
            event_id=item["id"],
            name=item["name"],
            event_date=item["date"],
            budget=item["budget"],
        )
        events.append(event)

    return events


def save_events(
    filename: str,
    events: list[Event],
) -> None:
    """Сохранить события в JSON."""
    data = []

    for event in events:
        data.append(
            {
                "id": event.id,
                "name": event.name,
                "date": event.date,
                "budget": event.budget,
            }
        )

    write_json(filename, data)


def load_participants(
    filename: str,
    events: list[Event],
) -> list[Participant]:
    """Загрузить участников из JSON."""
    data = read_json(filename)
    participants = []

    for item in data:
        event = find_event_by_id(
            events,
            item["event_id"],
        )

        if event is None:
            continue

        participant = Participant(
            participant_id=item["id"],
            event=event,
            name=item["name"],
        )
        participants.append(participant)

    return participants


def save_participants(
    filename: str,
    participants: list[Participant],
) -> None:
    """Сохранить участников в JSON."""
    data = []

    for participant in participants:
        data.append(
            {
                "id": participant.id,
                "event_id": participant.event.id,
                "name": participant.name,
            }
        )

    write_json(filename, data)


def load_tasks(
    filename: str,
    events: list[Event],
) -> list[Task]:
    """Загрузить задачи из JSON."""
    data = read_json(filename)
    tasks = []

    for item in data:
        event = find_event_by_id(
            events,
            item["event_id"],
        )

        if event is None:
            continue

        task = Task(
            task_id=item["id"],
            event=event,
            title=item["title"],
            completed=item.get("completed", False),
        )
        tasks.append(task)

    return tasks


def save_tasks(
    filename: str,
    tasks: list[Task],
) -> None:
    """Сохранить задачи в JSON."""
    data = []

    for task in tasks:
        data.append(
            {
                "id": task.id,
                "event_id": task.event.id,
                "title": task.title,
                "completed": task.completed,
            }
        )

    write_json(filename, data)


def load_expenses(
    filename: str,
    events: list[Event],
) -> list[Expense]:
    """Загрузить расходы из JSON."""
    data = read_json(filename)
    expenses = []

    for item in data:
        event = find_event_by_id(
            events,
            item["event_id"],
        )

        if event is None:
            continue

        expense = Expense(
            expense_id=item["id"],
            event=event,
            title=item["title"],
            amount=item["amount"],
        )
        expenses.append(expense)

    return expenses


def save_expenses(
    filename: str,
    expenses: list[Expense],
) -> None:
    """Сохранить расходы в JSON."""
    data = []

    for expense in expenses:
        data.append(
            {
                "id": expense.id,
                "event_id": expense.event.id,
                "title": expense.title,
                "amount": expense.amount,
            }
        )

    write_json(filename, data)

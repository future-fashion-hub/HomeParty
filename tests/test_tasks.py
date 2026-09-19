from models import Event, Task
from tasks import complete_task, get_pending_tasks


def test_task_creation() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    task = Task(
        1,
        event,
        "Купить торт",
    )

    assert task.id == 1
    assert task.title == "Купить торт"
    assert not task.completed
    assert task.event is event


def test_task_complete() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    task = Task(
        1,
        event,
        "Купить торт",
    )

    task.complete()

    assert task.completed


def test_complete_task() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    tasks = [
        Task(1, event, "Купить торт"),
    ]

    result = complete_task(
        tasks,
        1,
    )

    assert result
    assert tasks[0].completed


def test_get_pending_tasks() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    task_1 = Task(
        1,
        event,
        "Купить торт",
    )

    task_2 = Task(
        2,
        event,
        "Украсить комнату",
        True,
    )

    tasks = [
        task_1,
        task_2,
    ]

    result = get_pending_tasks(
        tasks,
        event,
    )

    assert len(result) == 1
    assert result[0] is task_1

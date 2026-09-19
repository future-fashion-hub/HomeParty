from models import Event, Task


def add_task(
    tasks: list[Task],
    event: Event,
    title: str,
) -> Task:
    """Добавить задачу подготовки."""
    task_id = len(tasks) + 1

    task = Task(
        task_id=task_id,
        event=event,
        title=title,
    )

    tasks.append(task)
    return task


def complete_task(
    tasks: list[Task],
    task_id: int,
) -> bool:
    """Отметить задачу как выполненную."""
    for task in tasks:
        if task.id == task_id:
            task.complete()
            return True

    return False


def get_pending_tasks(
    tasks: list[Task],
    event: Event,
) -> list[Task]:
    """Получить невыполненные задачи события."""
    return [
        task
        for task in tasks
        if task.event.id == event.id
        and not task.completed
    ]

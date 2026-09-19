def add_task(
    tasks: list[dict],
    event_id: int,
    title: str,
) -> dict:
    """Добавить задачу подготовки."""
    task_id = len(tasks) + 1

    task = {
        "id": task_id,
        "event_id": event_id,
        "title": title,
        "completed": False,
    }

    tasks.append(task)
    return task


def complete_task(
    tasks: list[dict],
    task_id: int,
) -> bool:
    """Отметить задачу как выполненную."""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return True

    return False


def get_pending_tasks(
    tasks: list[dict],
    event_id: int,
) -> list[dict]:
    """Получить невыполненные задачи события."""
    return [
        task
        for task in tasks
        if task["event_id"] == event_id
        and not task["completed"]
    ]

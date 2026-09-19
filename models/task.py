from .event import Event


class Task:
    """Задача подготовки события."""

    def __init__(
        self,
        task_id: int,
        event: Event,
        title: str,
        completed: bool = False,
    ) -> None:
        self.id = task_id
        self.event = event
        self.title = title
        self.completed = completed

    def complete(self) -> None:
        """Отметить задачу как выполненную."""
        self.completed = True

    def __str__(self) -> str:
        status = "выполнена" if self.completed else "не выполнена"

        return (
            f"{self.title} - {status}"
        )

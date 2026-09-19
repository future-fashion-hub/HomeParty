from .event import Event


class Expense:
    """Расход события."""

    def __init__(
        self,
        expense_id: int,
        event: Event,
        title: str,
        amount: float,
    ) -> None:
        self.id = expense_id
        self.event = event
        self.title = title
        self.amount = amount

    def __str__(self) -> str:
        return (
            f"{self.title}: "
            f"{self.amount} руб."
        )

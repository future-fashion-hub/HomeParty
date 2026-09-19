class Event:
    """Событие домашнего праздника."""

    def __init__(
        self,
        event_id: int,
        name: str,
        event_date: str,
        budget: float,
    ) -> None:
        self.id = event_id
        self.name = name
        self.date = event_date
        self.budget = budget

    def is_budget_enough(
        self,
        total_expenses: float,
    ) -> bool:
        """Проверить, хватает ли бюджета."""
        return total_expenses <= self.budget

    def __str__(self) -> str:
        return (
            f"{self.name} | "
            f"{self.date} | "
            f"бюджет: {self.budget} руб."
        )

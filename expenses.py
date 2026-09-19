def add_expense(
    expenses: list[dict],
    event_id: int,
    title: str,
    amount: float,
) -> dict:
    """Добавить расход."""
    expense_id = len(expenses) + 1

    expense = {
        "id": expense_id,
        "event_id": event_id,
        "title": title,
        "amount": amount,
    }

    expenses.append(expense)
    return expense


def get_total_expenses(
    expenses: list[dict],
    event_id: int,
) -> float:
    """Посчитать сумму расходов события."""
    total = 0.0

    for expense in expenses:
        if expense["event_id"] == event_id:
            total += expense["amount"]

    return total


def check_budget(
    budget: float,
    expenses: float,
) -> str:
    """Проверить, хватает ли бюджета."""
    if expenses <= budget:
        return "Бюджета достаточно"

    return "Расходы превышают бюджет"


def sort_expenses(
    expenses: list[dict],
) -> list[dict]:
    """Отсортировать расходы по сумме."""
    return sorted(
        expenses,
        key=lambda expense: expense["amount"],
        reverse=True,
    )

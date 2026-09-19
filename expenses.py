from models import Event, Expense


def add_expense(
    expenses: list[Expense],
    event: Event,
    title: str,
    amount: float,
) -> Expense:
    """Добавить расход."""
    expense_id = len(expenses) + 1

    expense = Expense(
        expense_id=expense_id,
        event=event,
        title=title,
        amount=amount,
    )

    expenses.append(expense)
    return expense


def get_total_expenses(
    expenses: list[Expense],
    event: Event,
) -> float:
    """Посчитать сумму расходов события."""
    total = 0.0

    for expense in expenses:
        if expense.event.id == event.id:
            total += expense.amount

    return total


def check_budget(
    event: Event,
    total_expenses: float,
) -> str:
    """Проверить, хватает ли бюджета."""
    if event.is_budget_enough(total_expenses):
        return "Бюджета достаточно"

    return "Расходы превышают бюджет"


def sort_expenses(
    expenses: list[Expense],
) -> list[Expense]:
    """Отсортировать расходы по сумме."""
    return sorted(
        expenses,
        key=lambda expense: expense.amount,
        reverse=True,
    )

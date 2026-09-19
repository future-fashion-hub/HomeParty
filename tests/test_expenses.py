from expenses import (
    add_expense,
    check_budget,
    get_total_expenses,
    sort_expenses,
)
from models import Event, Expense


def test_expense_creation() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    expense = Expense(
        1,
        event,
        "Торт",
        3000,
    )

    assert expense.id == 1
    assert expense.title == "Торт"
    assert expense.amount == 3000
    assert expense.event is event


def test_add_expense() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    expenses: list[Expense] = []

    expense = add_expense(
        expenses,
        event,
        "Торт",
        3000,
    )

    assert len(expenses) == 1
    assert expenses[0] is expense


def test_get_total_expenses() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    expenses = [
        Expense(1, event, "Торт", 3000),
        Expense(2, event, "Украшения", 2000),
    ]

    result = get_total_expenses(
        expenses,
        event,
    )

    assert result == 5000


def test_check_budget() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    assert check_budget(
        event,
        15000,
    ) == "Бюджета достаточно"

    assert check_budget(
        event,
        20000,
    ) == "Расходы превышают бюджет"


def test_sort_expenses() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    expenses = [
        Expense(1, event, "Украшения", 2000),
        Expense(2, event, "Торт", 3000),
    ]

    result = sort_expenses(expenses)

    assert result[0].amount == 3000
    assert result[1].amount == 2000

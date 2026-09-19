from expenses import (
    add_expense,
    check_budget,
    get_total_expenses,
)


def test_get_total_expenses():
    expenses = []

    add_expense(
        expenses,
        1,
        "Торт",
        3000,
    )

    add_expense(
        expenses,
        1,
        "Украшения",
        2000,
    )

    total = get_total_expenses(expenses, 1)

    assert total == 5000


def test_check_budget():
    result = check_budget(
        18000,
        15000,
    )

    assert result == "Бюджета достаточно"

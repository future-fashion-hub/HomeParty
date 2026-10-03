from html import escape

from django.http import HttpResponse

from homepage.views import page
from storage import load_events, load_expenses


def expense_list(request) -> HttpResponse:
    """Показать расходы и связанные события."""
    events = load_events("data/events.json")
    expenses = load_expenses("data/expenses.json", events)

    if expenses:
        rows = "".join(
            f"""
            <tr>
                <td>{expense.id}</td>
                <td>{escape(expense.title)}</td>
                <td>{escape(expense.event.name)}</td>
                <td class="text-end">{expense.amount:g} руб.</td>
            </tr>
            """
            for expense in expenses
        )
        body = f"""
        <div class="table-responsive shadow-sm">
            <table class="table table-striped table-hover mb-0">
                <thead class="table-primary">
                    <tr>
                        <th>ID</th><th>Расход</th><th>Событие</th>
                        <th class="text-end">Сумма</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """
    else:
        body = '<div class="alert alert-info">Расходов пока нет.</div>'

    content = f"<h1 class=\"mb-4\">Расходы</h1>{body}"
    return HttpResponse(page("Расходы HomeParty", content))

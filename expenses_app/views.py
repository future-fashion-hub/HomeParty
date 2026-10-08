from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from storage import load_events, load_expenses


def expense_list(request) -> HttpResponse:
    """Передать расходы и связанные события в шаблон."""
    data_dir = settings.BASE_DIR / "data"
    events = load_events(data_dir / "events.json")
    expenses = load_expenses(data_dir / "expenses.json", events)
    return render(
        request, "expenses_app/expense_list.html", {"expenses": expenses},
    )

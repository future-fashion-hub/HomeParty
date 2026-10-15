from django.http import HttpResponse
from django.shortcuts import render

from db.database import fetch_all
from db.presentation import with_event


def expense_list(request) -> HttpResponse:
    """Передать расходы и связанные события в шаблон."""
    expenses = [with_event(row) for row in fetch_all("expenses_with_events")]
    return render(
        request, "expenses_app/expense_list.html", {"expenses": expenses},
    )

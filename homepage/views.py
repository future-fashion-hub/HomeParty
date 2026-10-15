from django.http import HttpResponse
from django.shortcuts import render

from db.database import fetch_all


def index(request) -> HttpResponse:
    """Передать сводку данных SQLite в существующий шаблон."""
    context = {
        "events": fetch_all("events_list"),
        "participants": fetch_all("participants_with_events"),
        "tasks": fetch_all("tasks_with_events"),
        "expenses": fetch_all("expenses_with_events"),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception) -> HttpResponse:
    """Общий обработчик неизвестных URL и исключений Http404."""
    return render(request, "404.html", status=404)

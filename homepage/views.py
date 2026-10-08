from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from storage import load_events, load_expenses, load_participants, load_tasks


def index(request) -> HttpResponse:
    """Передать сводку JSON-данных в шаблон главной страницы."""
    data_dir = settings.BASE_DIR / "data"
    events = load_events(data_dir / "events.json")
    context = {
        "events": events,
        "participants": load_participants(
            data_dir / "participants.json", events,
        ),
        "tasks": load_tasks(data_dir / "tasks.json", events),
        "expenses": load_expenses(data_dir / "expenses.json", events),
    }
    return render(request, "homepage/index.html", context)

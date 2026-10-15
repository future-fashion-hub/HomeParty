from datetime import date
from decimal import Decimal, InvalidOperation

from django.http import HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one


def event_list(request) -> HttpResponse:
    """Показать все события либо результат поиска по бюджету."""
    minimum = request.GET.get("min_budget", "").strip()
    error = ""
    events = []
    if minimum:
        try:
            value = Decimal(minimum)
            if not value.is_finite() or not 0 <= value <= Decimal("1e12"):
                raise ValueError
            events = fetch_all("events_by_budget", (float(value),))
        except (InvalidOperation, ValueError):
            error = "Введите бюджет от 0 до 1 000 000 000 000."
    else:
        events = fetch_all("events_list")
    return render(
        request, "events_app/event_list.html",
        {"events": events, "min_budget": minimum, "error": error},
        status=400 if error else 200,
    )


def event_detail(request, event_id: int) -> HttpResponse:
    """Получить событие и агрегированные показатели из SQLite."""
    event = fetch_one("event_detail", (event_id,))
    context = {"event": event}

    if event is not None:
        metrics = fetch_one("event_metrics", (event_id, event_id))
        enough = event["budget"] >= metrics["spent"]
        context.update({
            "total_expenses": metrics["spent"],
            "budget_status": ("Бюджета достаточно" if enough
                              else "Расходы превышают бюджет"),
            "budget_enough": enough,
            "participant_total": metrics["participant_total"],
            "pending_tasks": fetch_all("event_pending_tasks", (event_id,)),
        })

    return render(
        request,
        "events_app/event_detail.html",
        context,
        status=404 if event is None else 200,
    )


def ready_events(request) -> HttpResponse:
    """Найти праздники на дату без незавершённых задач подготовки."""
    selected_date = request.GET.get("date", "").strip()
    events = []
    error = ""
    if selected_date:
        try:
            parsed = date.fromisoformat(selected_date)
            if parsed.isoformat() != selected_date:
                raise ValueError
        except ValueError:
            error = "Введите существующую дату в формате ГГГГ-ММ-ДД."
        else:
            events = fetch_all("ready_events", (selected_date,))
    return render(request, "events_app/ready.html", {
        "events": events, "selected_date": selected_date, "error": error,
    }, status=400 if error else 200)

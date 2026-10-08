from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from expenses import check_budget, get_total_expenses
from participants import count_participants
from storage import (
    find_event_by_id,
    load_events,
    load_expenses,
    load_participants,
    load_tasks,
)
from tasks import get_pending_tasks


def event_list(request) -> HttpResponse:
    """Передать события из JSON в шаблон списка."""
    events = load_events(settings.BASE_DIR / "data/events.json")
    return render(
        request, "events_app/event_list.html", {"events": events},
    )


def event_detail(request, event_id: int) -> HttpResponse:
    """Подготовить сведения о событии и связанных объектах."""
    data_dir = settings.BASE_DIR / "data"
    events = load_events(data_dir / "events.json")
    event = find_event_by_id(events, event_id)
    context = {"event": event}

    if event is not None:
        participants = load_participants(
            data_dir / "participants.json", events,
        )
        tasks = load_tasks(data_dir / "tasks.json", events)
        expenses = load_expenses(data_dir / "expenses.json", events)
        total = get_total_expenses(expenses, event)
        context.update({
            "total_expenses": total,
            "budget_status": check_budget(event, total),
            "budget_enough": event.is_budget_enough(total),
            "participant_total": count_participants(participants, event),
            "pending_tasks": get_pending_tasks(tasks, event),
        })

    return render(
        request,
        "events_app/event_detail.html",
        context,
        status=404 if event is None else 200,
    )

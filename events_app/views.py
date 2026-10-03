from html import escape

from django.http import HttpResponse, HttpResponseNotFound

from expenses import check_budget, get_total_expenses
from homepage.views import page
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
    """Показать список событий из JSON-хранилища."""
    events = load_events("data/events.json")

    if events:
        items = "".join(
            f"""
            <a class="list-group-item list-group-item-action"
               href="/events/{event.id}/">
                <div class="d-flex justify-content-between gap-3">
                    <span class="fw-semibold">{escape(event.name)}</span>
                    <span>{escape(event.date)}</span>
                </div>
                <small>Бюджет: {event.budget:g} руб.</small>
            </a>
            """
            for event in events
        )
    else:
        items = (
            '<div class="alert alert-info">'
            "События пока не добавлены."
            "</div>"
        )

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>События</h1>
        <a class="btn btn-outline-primary" href="/">На главную</a>
    </div>
    <div class="list-group shadow-sm">{items}</div>
    """

    return HttpResponse(page("События HomeParty", content))


def event_detail(request, event_id: int) -> HttpResponse:
    """Показать сведения о событии и связанных объектах."""
    events = load_events("data/events.json")
    event = find_event_by_id(events, event_id)

    if event is None:
        content = """
        <h1 class="text-danger">Событие не найдено</h1>
        <p>События с таким идентификатором нет.</p>
        <a class="btn btn-outline-secondary" href="/events/">
            К списку событий
        </a>
        """
        return HttpResponseNotFound(
            page("Событие не найдено", content)
        )

    participants = load_participants(
        "data/participants.json",
        events,
    )
    tasks = load_tasks("data/tasks.json", events)
    expenses = load_expenses("data/expenses.json", events)
    total = get_total_expenses(expenses, event)
    budget_status = check_budget(event, total)
    pending = get_pending_tasks(tasks, event)
    participant_total = count_participants(participants, event)
    budget_color = (
        "success"
        if event.is_budget_enough(total)
        else "danger"
    )

    content = f"""
    <div class="card shadow-sm">
        <div class="card-body p-4">
            <h1 class="card-title">{escape(event.name)}</h1>
            <p class="text-secondary">Дата: {escape(event.date)}</p>
            <div class="row g-3 mt-2">
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <strong>Бюджет</strong>
                        <div>{event.budget:g} руб.</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <strong>Расходы</strong>
                        <div>{total:g} руб.</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <strong>Участники</strong>
                        <div>{participant_total}</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <strong>Открытые задачи</strong>
                        <div>{len(pending)}</div>
                    </div>
                </div>
            </div>
            <p class="mt-4 mb-0">
                <span class="badge text-bg-{budget_color}">
                    {budget_status}
                </span>
            </p>
        </div>
    </div>
    <a class="btn btn-outline-secondary mt-4" href="/events/">
        К списку событий
    </a>
    """

    return HttpResponse(
        page(f"Событие {event.name}", content)
    )

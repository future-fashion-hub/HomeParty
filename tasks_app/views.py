from django.http import HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one
from db.presentation import with_event


def task_list(request) -> HttpResponse:
    """Показать все задачи с данными связанного события из JOIN."""
    tasks = [with_event(row) for row in fetch_all("tasks_with_events")]
    return render(request, "tasks_app/task_list.html", {"tasks": tasks})


def task_detail(request, task_id: int) -> HttpResponse:
    """Показать задачу либо шаблонное сообщение с HTTP-кодом 404."""
    task = with_event(fetch_one("task_detail", (task_id,)))
    return render(
        request,
        "tasks_app/task_detail.html",
        {"task": task},
        status=404 if task is None else 200,
    )


def pending_tasks(request) -> HttpResponse:
    """Показать результат SQL-фильтра completed = 0."""
    return render(request, "tasks_app/pending.html", {
        "tasks": fetch_all("pending_tasks"),
    })

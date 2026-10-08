from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from storage import load_events, load_tasks


def task_list(request) -> HttpResponse:
    """Показать задачи подготовки и их статус через шаблон."""
    data_dir = settings.BASE_DIR / "data"
    events = load_events(data_dir / "events.json")
    tasks = load_tasks(data_dir / "tasks.json", events)
    return render(request, "tasks_app/task_list.html", {"tasks": tasks})


def task_detail(request, task_id: int) -> HttpResponse:
    """Показать задачу либо шаблонное сообщение с HTTP-кодом 404."""
    data_dir = settings.BASE_DIR / "data"
    events = load_events(data_dir / "events.json")
    tasks = load_tasks(data_dir / "tasks.json", events)
    task = next((item for item in tasks if item.id == task_id), None)
    return render(
        request,
        "tasks_app/task_detail.html",
        {"task": task},
        status=404 if task is None else 200,
    )

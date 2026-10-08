import os

import django
import pytest


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homeparty.settings")
django.setup()

from django.contrib.staticfiles import finders  # noqa: E402
from django.template.loader import render_to_string  # noqa: E402
from django.test import Client  # noqa: E402
from django.urls import reverse  # noqa: E402

from models import Event, Task  # noqa: E402


@pytest.mark.parametrize(
    ("name", "kwargs", "path"),
    [
        ("homepage:index", {}, "/"),
        ("events_app:event_list", {}, "/events/"),
        ("events_app:event_detail", {"event_id": 1}, "/events/1/"),
        ("participants_app:participant_list", {}, "/participants/"),
        ("tasks_app:task_list", {}, "/tasks/"),
        ("tasks_app:task_detail", {"task_id": 1}, "/tasks/1/"),
        ("expenses_app:expense_list", {}, "/expenses/"),
    ],
)
def test_namespaced_routes(name, kwargs, path) -> None:
    assert reverse(name, kwargs=kwargs) == path
    response = Client().get(path)
    assert response.status_code == 200
    html = response.content.decode()
    assert 'id="current-year"' in html
    assert "/static/homepage/css/style.css" in html
    assert "/static/homepage/img/logo.svg" in html
    assert "/static/homepage/js/main.js" in html


@pytest.mark.parametrize(
    ("path", "message", "back_link"),
    [
        ("/events/9999/", "Событие не найдено", "/events/"),
        ("/tasks/9999/", "Задача не найдена", "/tasks/"),
    ],
)
def test_template_404(path, message, back_link) -> None:
    response = Client().get(path)
    assert response.status_code == 404
    html = response.content.decode()
    assert message in html
    assert f'href="{back_link}"' in html
    assert 'id="current-year"' in html


@pytest.mark.parametrize(
    ("template", "key", "message"),
    [
        ("events_app/event_list.html", "events",
         "События пока не добавлены."),
        ("tasks_app/task_list.html", "tasks", "Задач пока нет."),
        ("participants_app/participant_list.html", "participants",
         "Участников пока нет."),
        ("expenses_app/expense_list.html", "expenses", "Расходов пока нет."),
    ],
)
def test_empty_collections(template, key, message) -> None:
    html = render_to_string(template, {key: []})
    assert message in html


@pytest.mark.parametrize(
    ("completed", "expected"),
    [(True, "Выполнена"), (False, "В работе")],
)
def test_task_status_in_list_and_detail(completed, expected) -> None:
    event = Event(1, "Праздник", "2026-10-10", 5000)
    task = Task(1, event, "Подготовить праздник", completed)
    for template, context in [
        ("tasks_app/task_list.html", {"tasks": [task]}),
        ("tasks_app/task_detail.html", {"task": task}),
    ]:
        html = render_to_string(template, context)
        assert expected in html
        assert 'href="/events/1/"' in html


def test_event_filters_and_autoescaping() -> None:
    event = Event(1, "", "2026-10-10", 123.456)
    html = render_to_string(
        "events_app/event_list.html", {"events": [event]},
    )
    assert "Без названия" in html
    assert "Всего событий: 1" in html
    assert "123,46" in html

    event.name = '<script>alert("test")</script>'
    html = render_to_string(
        "events_app/event_list.html", {"events": [event]},
    )
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html


@pytest.mark.parametrize(
    "asset",
    [
        "homepage/css/style.css",
        "homepage/img/logo.svg",
        "homepage/js/main.js",
    ],
)
def test_static_resources_available(asset) -> None:
    assert finders.find(asset) is not None

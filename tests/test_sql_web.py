import os
from contextlib import closing

import django
import pytest

from db import database
from db.import_json import import_data


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homeparty.settings")
django.setup()

from django.test import Client  # noqa: E402


@pytest.fixture
def sql_web(tmp_path, monkeypatch):
    path = tmp_path / "web.sqlite"
    import_data(db_path=path)
    monkeypatch.setattr(database, "DB_PATH", path)
    return Client()


@pytest.mark.parametrize("url, text", [
    ("/events/?min_budget=20000", "Новоселье"),
    ("/tasks/pending/", "Украсить комнату"),
    ("/statistics/", "Статистика праздников"),
    ("/statistics/?min_tasks=1", "Событий с таким числом"),
    ("/events/ready/", "Готовность праздников"),
    ("/events/ready/?date=2026-10-10", "готовых событий нет"),
])
def test_sql_scenarios(sql_web, url, text):
    response = sql_web.get(url)
    assert response.status_code == 200
    assert text in response.content.decode()


@pytest.mark.parametrize("url", [
    "/events/?min_budget=-1", "/events/?min_budget=NaN",
    "/events/?min_budget=Infinity", "/events/?min_budget=bad",
    "/events/ready/?date=2026-02-30", "/events/ready/?date=20261010",
    "/events/ready/?date=' OR 1=1 --", "/statistics/?min_tasks=bad",
    "/statistics/?min_tasks=-1",
])
def test_invalid_filters_are_not_server_errors(sql_web, url):
    assert sql_web.get(url).status_code == 400


def test_db_changes_reach_browser_response(sql_web):
    with closing(database.get_connection()) as connection:
        connection.execute("UPDATE events SET name=? WHERE id=?",
                           ("Название из SQLite", 1))
        connection.execute("UPDATE tasks SET completed=1 WHERE event_id=1")
        connection.commit()
    assert "Название из SQLite" in sql_web.get("/events/").content.decode()
    ready = sql_web.get("/events/ready/?date=2026-10-10").content.decode()
    assert "Название из SQLite" in ready
    pending = sql_web.get("/tasks/pending/").content.decode()
    assert "Заказать торт" not in pending


def test_every_saved_query_is_used_by_web(sql_web, monkeypatch):
    import events_app.views
    import expenses_app.views
    import homepage.statistics
    import homepage.views
    import participants_app.views
    import tasks_app.views

    called = set()

    def spy(function):
        def wrapper(name, *args, **kwargs):
            called.add(name)
            return function(name, *args, **kwargs)
        return wrapper

    for module in (events_app.views, expenses_app.views, homepage.statistics,
                   homepage.views, participants_app.views, tasks_app.views):
        for name in ("fetch_all", "fetch_one"):
            if hasattr(module, name):
                monkeypatch.setattr(module, name, spy(getattr(module, name)))
    for url in ("/", "/events/", "/events/?min_budget=20000", "/events/1/",
                "/tasks/", "/tasks/1/", "/tasks/pending/", "/participants/",
                "/expenses/", "/statistics/",
                "/events/ready/?date=2026-10-10"):
        assert sql_web.get(url).status_code == 200
    assert called == set(database.QUERIES)

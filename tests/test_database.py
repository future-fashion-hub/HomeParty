from contextlib import closing
import json
from pathlib import Path
import shutil
import sqlite3

import pytest

from db import database
from db.check_queries import EXAMPLES
from db.import_json import import_data


SOURCE = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture
def sql_db(tmp_path, monkeypatch):
    path = tmp_path / "test.sqlite"
    import_data(SOURCE, path)
    monkeypatch.setattr(database, "DB_PATH", path)
    return path


def test_schema_and_import_are_repeatable(sql_db):
    before = database.fetch_one("overview")
    database.create_schema(sql_db)
    import_data(SOURCE, sql_db)
    assert tuple(database.fetch_one("overview")) == tuple(before)
    assert tuple(before) == (2, 3, 3, 3, 0)
    with closing(database.get_connection()) as connection:
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert not connection.execute("PRAGMA foreign_key_check").fetchall()


def test_all_saved_queries_run(sql_db):
    assert len(database.QUERIES) == 17
    for name in database.QUERIES:
        rows = database.fetch_all(name, EXAMPLES.get(name, ()))
        assert all(isinstance(row, sqlite3.Row) for row in rows)


def test_queries_match_source_and_join_values(sql_db):
    for name, key, filename in [
        ("events_list", "name", "events"),
        ("tasks_with_events", "title", "tasks"),
        ("expenses_with_events", "title", "expenses"),
        ("participants_with_events", "name", "participants"),
        ("users_list", "name", "users"),
    ]:
        source = json.loads((SOURCE / f"{filename}.json").read_text("utf-8"))
        assert sorted(row[key] for row in database.fetch_all(name)) == sorted(
            row[key] for row in source
        )
    assert database.fetch_one("task_detail", (1,))["event_name"] == (
        "День рождения"
    )
    assert len(database.fetch_all("events_by_budget", (20000,))) == 1
    assert len(database.fetch_all("pending_tasks")) == 2
    assert database.fetch_one("expense_totals")["total"] == 10500


@pytest.mark.parametrize("table, sql", [
    ("tasks", "INSERT INTO tasks VALUES (90, 999, 'invalid', 0)"),
    ("tasks", "INSERT INTO tasks VALUES (90, 1, 'invalid', 2)"),
    ("expenses", "INSERT INTO expenses VALUES (90, 1, 'invalid', -1)"),
    ("events", "INSERT INTO events VALUES (1, 'duplicate', '2026-01-01', 0)"),
])
def test_integrity_constraints(sql_db, table, sql):
    with closing(database.get_connection()) as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(sql)


def test_optional_email_can_be_null(sql_db):
    with closing(database.get_connection()) as connection:
        connection.execute("INSERT INTO users VALUES (?, ?, ?)",
                           (1, "User", None))
        connection.commit()
    assert database.fetch_one("users_list")["email"] is None


def test_import_is_atomic_on_foreign_key_error(tmp_path):
    source = tmp_path / "json"
    shutil.copytree(SOURCE, source, ignore=shutil.ignore_patterns("*.sqlite"))
    tasks = json.loads((source / "tasks.json").read_text("utf-8"))
    tasks[0]["event_id"] = 999
    (source / "tasks.json").write_text(json.dumps(tasks), encoding="utf-8")
    path = tmp_path / "invalid.sqlite"
    with pytest.raises(sqlite3.IntegrityError):
        import_data(source, path)
    assert tuple(database.fetch_one("overview", db_path=path)) == (0,) * 5


def test_groups_keep_events_without_children(sql_db):
    with closing(database.get_connection()) as connection:
        connection.execute("INSERT INTO events VALUES (?, ?, ?, ?)",
                           (3, "Без задач", "2026-10-10", 100))
        connection.commit()
    group = database.fetch_all("tasks_by_event")[-1]
    assert group["task_count"] == group["pending_count"] == 0
    assert database.fetch_all("expenses_by_event")[-1]["spent"] == 0
    assert database.fetch_all("ready_events", ("2026-10-10",))[0]["id"] == 3
    assert len(database.fetch_all("busy_events", (0,))) == 2
    assert not database.fetch_all("busy_events", (1,))


def test_bound_parameter_does_not_change_query(sql_db):
    assert not database.fetch_all("event_detail", ("1 OR 1=1",))
    assert not database.fetch_all("ready_events", ("' OR 1=1 --",))
    assert len(database.fetch_all("events_list")) == 2


def test_empty_database_has_zero_aggregates(tmp_path):
    path = tmp_path / "empty.sqlite"
    database.create_schema(path)
    assert tuple(database.fetch_one("overview", db_path=path)) == (0,) * 5
    totals = database.fetch_one("expense_totals", db_path=path)
    assert tuple(totals) == (0,) * 5
    assert not database.fetch_all("tasks_by_event", db_path=path)

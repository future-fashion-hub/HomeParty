"""Проверка каждого запроса и его выполнение в CLI стандартной sqlite3."""

import argparse
from contextlib import closing
import subprocess
import sys

from db.database import DB_PATH, QUERIES, get_connection


EXAMPLES = {
    "events_by_budget": (20000,),
    "busy_events": (0,),
    "ready_events": ("2026-10-10",),
    "event_detail": (1,),
    "task_detail": (1,),
    "event_metrics": (1, 1),
    "event_pending_tasks": (1,),
}


def check_queries(db_path=DB_PATH, cli=False):
    with closing(get_connection(db_path)) as connection:
        assert not connection.execute("PRAGMA foreign_key_check").fetchall()
        for name, query in QUERIES.items():
            expanded = []
            connection.set_trace_callback(expanded.append)
            rows = connection.execute(query, EXAMPLES.get(name, ())).fetchall()
            connection.set_trace_callback(None)
            print(f"{name}: {len(rows)} rows")
            if cli:
                # SQLite сама раскрыла параметры; пользовательский ввод здесь
                # не собирается в SQL. CLI повторяет только тестовый SELECT.
                result = subprocess.run(
                    [sys.executable, "-X", "utf8", "-m", "sqlite3",
                     str(db_path), expanded[-1]],
                    check=True, capture_output=True, text=True,
                    encoding="utf-8",
                )
                print(result.stdout.strip() or "(empty result)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", action="store_true")
    arguments = parser.parse_args()
    check_queries(cli=arguments.cli)

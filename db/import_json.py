"""Повторяемый транзакционный импорт исходных данных ПР1–ПР6."""

import argparse
from contextlib import closing
import json
from pathlib import Path

from db.database import BASE_DIR, DB_PATH, create_schema, get_connection


# Имена таблиц и SQL фиксированы кодом, пользовательские значения — только ?.
IMPORTS = (
    ("events", ("id", "name", "date", "budget"),
     "INSERT INTO events VALUES (?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET "
     "name=excluded.name, date=excluded.date, budget=excluded.budget"),
    ("users", ("id", "name", "email"),
     "INSERT INTO users VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET "
     "name=excluded.name, email=excluded.email"),
    ("participants", ("id", "event_id", "name"),
     "INSERT INTO participants VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET "
     "event_id=excluded.event_id, name=excluded.name"),
    ("tasks", ("id", "event_id", "title", "completed"),
     "INSERT INTO tasks VALUES (?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET "
     "event_id=excluded.event_id, title=excluded.title, "
     "completed=excluded.completed"),
    ("expenses", ("id", "event_id", "title", "amount"),
     "INSERT INTO expenses VALUES (?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET "
     "event_id=excluded.event_id, title=excluded.title, "
     "amount=excluded.amount"),
)


def import_data(data_dir=None, db_path=None):
    """Родители импортируются первыми, ошибка откатывает все вставки."""
    source = Path(data_dir) if data_dir is not None else BASE_DIR / "data"
    batches = []
    counts = {}
    for table, columns, query in IMPORTS:
        items = json.loads((source / f"{table}.json").read_text("utf-8"))
        if not isinstance(items, list):
            raise ValueError(f"Expected a list: {table}.json")
        values = [tuple(item.get(column) if column == "email"
                        else item.get(column, False) if column == "completed"
                        else item[column] for column in columns)
                  for item in items]
        batches.append((query, values))
        counts[table] = len(values)

    create_schema(db_path)
    with closing(get_connection(db_path)) as connection:
        with connection:
            for query, values in batches:
                connection.executemany(query, values)
            connection.commit()
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DB_PATH)
    parser.add_argument("--source", type=Path, default=BASE_DIR / "data")
    arguments = parser.parse_args()
    print(import_data(arguments.source, arguments.database))
    print(f"Imported into: {arguments.database.resolve()}")

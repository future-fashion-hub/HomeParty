"""Подключения SQLite и единый каталог SQL-запросов."""

from contextlib import closing
from pathlib import Path
import re
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data/homeparty.sqlite"
SCHEMA_PATH = BASE_DIR / "sql/schema.sql"
QUERY_PATH = BASE_DIR / "sql/queries.sql"


def get_connection(db_path=None):
    """Открыть БД с именованными строками и контролем внешних ключей."""
    connection = sqlite3.connect(db_path if db_path is not None else DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def load_queries():
    """Прочитать SQL из файла: имена запросов заданы комментариями name."""
    parts = re.split(
        r"^-- name: (\w+)\s*$", QUERY_PATH.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    return dict(zip(parts[1::2], parts[2::2]))


QUERIES = load_queries()


def fetch_all(name, parameters=(), db_path=None):
    """Выполнить сохранённый запрос; значения передаются отдельно от SQL."""
    with closing(get_connection(db_path)) as connection:
        return connection.execute(QUERIES[name], parameters).fetchall()


def fetch_one(name, parameters=(), db_path=None):
    with closing(get_connection(db_path)) as connection:
        return connection.execute(QUERIES[name], parameters).fetchone()


def create_schema(db_path=None):
    """Создать отсутствующие таблицы без удаления существующих записей."""
    with closing(get_connection(db_path)) as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.commit()


if __name__ == "__main__":
    create_schema()
    print(f"Schema ready: {DB_PATH}")

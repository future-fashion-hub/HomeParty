-- HomeParty, ПР7. Отдельная предметная БД, не Django db.sqlite3.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    budget REAL NOT NULL CHECK (budget >= 0)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    title TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1))
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    title TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0)
);

CREATE INDEX IF NOT EXISTS tasks_event_state ON tasks(event_id, completed);
CREATE INDEX IF NOT EXISTS expenses_event ON expenses(event_id);
CREATE INDEX IF NOT EXISTS participants_event ON participants(event_id);

import json
from pathlib import Path
from typing import Any


def load_json(filename: str) -> list[dict[str, Any]]:
    """Загрузить данные из JSON-файла."""
    path = Path(filename)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_json(
    filename: str,
    data: list[dict[str, Any]],
) -> None:
    """Сохранить данные в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )

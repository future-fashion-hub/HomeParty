"""Адаптация именованных JOIN-строк к вложенному контексту шаблонов ПР6."""


def with_event(row):
    if row is None:
        return None
    result = dict(row)
    result["event"] = {
        "id": row["event_id"],
        "name": row["event_name"],
        "date": row["event_date"] if "event_date" in row.keys() else "",
    }
    return result

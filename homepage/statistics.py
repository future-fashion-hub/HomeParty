from django.shortcuts import render

from db.database import fetch_all, fetch_one


def statistics(request):
    """Показать агрегаты, группировки, HAVING и список пользователей."""
    raw_threshold = request.GET.get("min_tasks", "0")
    try:
        threshold = int(raw_threshold)
        if not 0 <= threshold <= 1000000:
            raise ValueError
    except ValueError:
        return render(request, "homepage/statistics.html", {
            "error": "Введите целый порог от 0 до 1 000 000.",
        }, status=400)
    return render(request, "homepage/statistics.html", {
        "overview": fetch_one("overview"),
        "totals": fetch_one("expense_totals"),
        "task_groups": fetch_all("tasks_by_event"),
        "expense_groups": fetch_all("expenses_by_event"),
        "busy_events": fetch_all("busy_events", (threshold,)),
        "users": fetch_all("users_list"),
        "threshold": threshold,
    })

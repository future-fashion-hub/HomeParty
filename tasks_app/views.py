from html import escape

from django.http import HttpResponse

from homepage.views import page
from storage import load_events, load_tasks


def task_list(request) -> HttpResponse:
    """Показать задачи подготовки и их статус."""
    events = load_events("data/events.json")
    tasks = load_tasks("data/tasks.json", events)

    if tasks:
        rows = "".join(
            f"""
            <tr>
                <td>{task.id}</td>
                <td>{escape(task.title)}</td>
                <td>{escape(task.event.name)}</td>
                <td>
                    <span class="badge text-bg-{
                        'success' if task.completed else 'warning'
                    }">
                        {'Выполнена' if task.completed else 'В работе'}
                    </span>
                </td>
            </tr>
            """
            for task in tasks
        )
        body = f"""
        <div class="table-responsive shadow-sm">
            <table class="table table-striped table-hover mb-0">
                <thead class="table-primary">
                    <tr>
                        <th>ID</th><th>Задача</th><th>Событие</th><th>Статус</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """
    else:
        body = '<div class="alert alert-info">Задач пока нет.</div>'

    content = f"<h1 class=\"mb-4\">Задачи подготовки</h1>{body}"
    return HttpResponse(page("Задачи HomeParty", content))

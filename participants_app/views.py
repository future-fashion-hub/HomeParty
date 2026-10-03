from html import escape

from django.http import HttpResponse

from homepage.views import page
from storage import load_events, load_participants


def participant_list(request) -> HttpResponse:
    """Показать участников и связанные события."""
    events = load_events("data/events.json")
    participants = load_participants(
        "data/participants.json",
        events,
    )

    if participants:
        rows = "".join(
            f"""
            <tr>
                <td>{participant.id}</td>
                <td>{escape(participant.name)}</td>
                <td>
                    <a href="/events/{participant.event.id}/">
                        {escape(participant.event.name)}
                    </a>
                </td>
            </tr>
            """
            for participant in participants
        )
        body = f"""
        <div class="table-responsive shadow-sm">
            <table class="table table-striped table-hover mb-0">
                <thead class="table-primary">
                    <tr><th>ID</th><th>Имя</th><th>Событие</th></tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """
    else:
        body = '<div class="alert alert-info">Участников пока нет.</div>'

    content = f"<h1 class=\"mb-4\">Участники</h1>{body}"
    return HttpResponse(page("Участники HomeParty", content))

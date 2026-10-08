from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from storage import load_events, load_participants


def participant_list(request) -> HttpResponse:
    """Передать участников и связанные события в шаблон."""
    data_dir = settings.BASE_DIR / "data"
    events = load_events(data_dir / "events.json")
    participants = load_participants(data_dir / "participants.json", events)
    return render(
        request,
        "participants_app/participant_list.html",
        {"participants": participants},
    )

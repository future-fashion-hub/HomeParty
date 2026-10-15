from django.http import HttpResponse
from django.shortcuts import render

from db.database import fetch_all
from db.presentation import with_event


def participant_list(request) -> HttpResponse:
    """Передать участников и связанные события в шаблон."""
    participants = [with_event(row)
                    for row in fetch_all("participants_with_events")]
    return render(
        request,
        "participants_app/participant_list.html",
        {"participants": participants},
    )

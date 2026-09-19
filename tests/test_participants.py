from models import Event, Participant
from participants import add_participant, count_participants


def test_participant_creation() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    participant = Participant(
        1,
        event,
        "Иван",
    )

    assert participant.id == 1
    assert participant.name == "Иван"
    assert participant.event is event


def test_add_participant() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    participants: list[Participant] = []

    participant = add_participant(
        participants,
        event,
        "Иван",
    )

    assert len(participants) == 1
    assert participants[0] is participant


def test_count_participants() -> None:
    event = Event(
        1,
        "День рождения",
        "2026-10-10",
        18000,
    )

    participants = [
        Participant(1, event, "Иван"),
        Participant(2, event, "Анна"),
    ]

    assert count_participants(
        participants,
        event,
    ) == 2

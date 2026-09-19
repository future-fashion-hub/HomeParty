from models import Event, Participant


def add_participant(
    participants: list[Participant],
    event: Event,
    name: str,
) -> Participant:
    """Добавить участника к событию."""
    participant_id = len(participants) + 1

    participant = Participant(
        participant_id=participant_id,
        event=event,
        name=name,
    )

    participants.append(participant)
    return participant


def find_participant(
    participants: list[Participant],
    query: str,
) -> list[Participant]:
    """Найти участника по имени."""
    query = query.lower()

    return [
        participant
        for participant in participants
        if query in participant.name.lower()
    ]


def count_participants(
    participants: list[Participant],
    event: Event,
) -> int:
    """Посчитать участников конкретного события."""
    count = 0

    for participant in participants:
        if participant.event.id == event.id:
            count += 1

    return count

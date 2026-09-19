def add_participant(
    participants: list[dict],
    event_id: int,
    name: str,
) -> dict:
    """Добавить участника к событию."""
    participant_id = len(participants) + 1

    participant = {
        "id": participant_id,
        "event_id": event_id,
        "name": name,
    }

    participants.append(participant)
    return participant


def find_participant(
    participants: list[dict],
    query: str,
) -> list[dict]:
    """Найти участника по имени."""
    query = query.lower()

    return [
        participant
        for participant in participants
        if query in participant["name"].lower()
    ]


def count_participants(
    participants: list[dict],
    event_id: int,
) -> int:
    """Посчитать участников конкретного события."""
    count = 0

    for participant in participants:
        if participant["event_id"] == event_id:
            count += 1

    return count

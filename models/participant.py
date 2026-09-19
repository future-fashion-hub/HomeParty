from .event import Event


class Participant:
    """Участник события."""

    def __init__(
        self,
        participant_id: int,
        event: Event,
        name: str,
    ) -> None:
        self.id = participant_id
        self.event = event
        self.name = name

    def __str__(self) -> str:
        return (
            f"{self.name} "
            f"(событие: {self.event.name})"
        )

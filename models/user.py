class User:
    """Пользователь приложения."""

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
    ) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"

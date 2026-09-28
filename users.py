from models import User


def add_user(
    users: list[User],
    name: str,
    email: str,
) -> User:
    """Добавить нового пользователя."""
    user_id = len(users) + 1

    user = User(
        user_id=user_id,
        name=name,
        email=email,
    )

    users.append(user)
    return user


def find_user(
    users: list[User],
    query: str,
) -> list[User]:
    """Найти пользователей по имени или электронной почте."""
    query = query.lower()

    return [
        user
        for user in users
        if query in user.name.lower()
        or query in user.email.lower()
    ]

from models import User
from users import add_user, find_user


def test_user_creation() -> None:
    user = User(
        user_id=1,
        name="Иван",
        email="ivan@example.com",
    )

    assert user.id == 1
    assert user.name == "Иван"
    assert user.email == "ivan@example.com"


def test_user_str() -> None:
    user = User(1, "Иван", "ivan@example.com")

    assert "Иван" in str(user)
    assert "ivan@example.com" in str(user)


def test_add_user() -> None:
    users: list[User] = []

    user = add_user(
        users,
        "Иван",
        "ivan@example.com",
    )

    assert len(users) == 1
    assert users[0] is user


def test_find_user() -> None:
    users = [
        User(1, "Иван", "ivan@example.com"),
        User(2, "Анна", "anna@example.com"),
    ]

    by_name = find_user(users, "иван")
    by_email = find_user(users, "anna@")

    assert by_name == [users[0]]
    assert by_email == [users[1]]

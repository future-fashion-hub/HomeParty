import os

import django


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "homeparty.settings",
)
django.setup()

from django.test import Client  # noqa: E402


client = Client()


def test_homepage() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "HomeParty" in response.content.decode("utf-8")


def test_event_list() -> None:
    response = client.get("/events/")

    assert response.status_code == 200
    assert "События" in response.content.decode("utf-8")


def test_event_detail() -> None:
    response = client.get("/events/1/")

    assert response.status_code == 200
    assert "День рождения" in response.content.decode("utf-8")


def test_missing_event_returns_404() -> None:
    response = client.get("/events/999/")

    assert response.status_code == 404
    assert "Событие не найдено" in response.content.decode("utf-8")


def test_domain_pages() -> None:
    for url in ("/participants/", "/tasks/", "/expenses/"):
        response = client.get(url)
        assert response.status_code == 200

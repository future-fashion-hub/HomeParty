import os

import django
import pytest


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homeparty.settings")
django.setup()

from django.http import Http404  # noqa: E402
from django.test import Client, override_settings  # noqa: E402
from django.urls import get_resolver  # noqa: E402

from homepage.views import page_not_found  # noqa: E402


@pytest.mark.parametrize(
    "path",
    ["/nonexistent/", "/events/abc/", "/tasks/abc/", "/events/1/extra/"],
)
@override_settings(DEBUG=False)
def test_unknown_route_uses_custom_404(path) -> None:
    response = Client().get(path)
    html = response.content.decode()
    assert response.status_code == 404
    assert "404 — Страница не найдена" in html
    assert 'href="/"' in html
    assert "/static/homepage/css/style.css" in html
    assert 'id="current-year"' in html
    assert "urlpatterns" not in html


def test_handler_registered_in_root_urlconf() -> None:
    assert get_resolver().resolve_error_handler(404) is page_not_found


@override_settings(DEBUG=False)
def test_http404_from_view_uses_global_handler(monkeypatch) -> None:
    def missing_data(*args, **kwargs):
        raise Http404("Internal exception details must not be displayed")

    monkeypatch.setattr("events_app.views.load_events", missing_data)
    response = Client().get("/events/")
    html = response.content.decode()
    assert response.status_code == 404
    assert "404 — Страница не найдена" in html
    assert "Internal exception details" not in html


@override_settings(DEBUG=True)
def test_debug_mode_keeps_django_diagnostics() -> None:
    response = Client().get("/nonexistent/")
    assert response.status_code == 404
    assert "Using the URLconf" in response.content.decode()


@pytest.mark.parametrize("path", ["/", "/events/1/"])
@override_settings(DEBUG=False)
def test_known_routes_work_without_debug(path) -> None:
    assert Client().get(path).status_code == 200


@pytest.mark.parametrize(
    ("path", "message"),
    [("/events/999/", "Событие не найдено"),
     ("/tasks/999/", "Задача не найдена")],
)
@override_settings(DEBUG=False)
def test_missing_objects_keep_specific_404(path, message) -> None:
    response = Client().get(path)
    assert response.status_code == 404
    assert message in response.content.decode()

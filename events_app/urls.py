from django.urls import path

from . import views


app_name = "events_app"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("ready/", views.ready_events, name="ready"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
]

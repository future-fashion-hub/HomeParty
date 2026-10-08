from django.urls import path

from . import views


app_name = "participants_app"

urlpatterns = [
    path("", views.participant_list, name="participant_list"),
]

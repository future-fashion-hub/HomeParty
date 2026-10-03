from django.urls import path

from . import views


urlpatterns = [
    path("", views.participant_list, name="participant_list"),
]

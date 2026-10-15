from django.urls import path

from . import views
from .statistics import statistics


app_name = "homepage"

urlpatterns = [
    path("", views.index, name="index"),
    path("statistics/", statistics, name="statistics"),
]

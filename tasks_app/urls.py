from django.urls import path

from . import views


app_name = "tasks_app"

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("<int:task_id>/", views.task_detail, name="task_detail"),
]

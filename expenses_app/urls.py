from django.urls import path

from . import views


app_name = "expenses_app"

urlpatterns = [
    path("", views.expense_list, name="expense_list"),
]

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("events/", include("events_app.urls")),
    path("participants/", include("participants_app.urls")),
    path("tasks/", include("tasks_app.urls")),
    path("expenses/", include("expenses_app.urls")),
]

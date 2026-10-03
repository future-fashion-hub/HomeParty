from django.apps import AppConfig


class TasksAppConfig(AppConfig):
    """Настройки приложения задач."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks_app"

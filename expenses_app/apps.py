from django.apps import AppConfig


class ExpensesAppConfig(AppConfig):
    """Настройки приложения расходов."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "expenses_app"

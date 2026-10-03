from html import escape

from django.http import HttpResponse

from storage import (
    load_events,
    load_expenses,
    load_participants,
    load_tasks,
)


def page(title: str, content: str) -> str:
    """Сформировать общую HTML-страницу с Bootstrap-навигацией."""
    safe_title = escape(title)
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    fallback_css = """
    * { box-sizing: border-box; }
    body {
        margin: 0;
        background: #f8f9fa;
        color: #212529;
        font-family: Arial, sans-serif;
        line-height: 1.5;
    }
    a { color: #0d6efd; }
    .container {
        width: min(1120px, calc(100% - 32px));
        margin: 0 auto;
    }
    .navbar { padding: 12px 0; }
    .navbar-dark { color: white; }
    .bg-primary { background: #0d6efd; }
    .navbar .container, .d-flex { display: flex; }
    .navbar .container { align-items: center; }
    .navbar-brand {
        color: white;
        font-size: 20px;
        margin-right: auto;
        text-decoration: none;
    }
    .navbar-nav { display: flex; }
    .nav-link {
        color: rgba(255, 255, 255, .78);
        padding: 8px;
        text-decoration: none;
    }
    .py-5 { padding-top: 48px; padding-bottom: 48px; }
    .mb-0 { margin-bottom: 0; }
    .mb-4 { margin-bottom: 24px; }
    .mb-5 { margin-bottom: 48px; }
    .mt-2 { margin-top: 8px; }
    .mt-4 { margin-top: 24px; }
    .p-3 { padding: 16px; }
    .p-4 { padding: 24px; }
    .fw-semibold { font-weight: 600; }
    .lead { font-size: 20px; }
    .display-4 { font-size: 48px; margin: 0 0 8px; }
    .display-6 { font-size: 36px; }
    .h5 { font-size: 20px; }
    .text-decoration-none { text-decoration: none; }
    .text-secondary { color: #6c757d; }
    .text-dark { color: #212529; }
    .text-danger { color: #dc3545; }
    .text-primary { color: #0d6efd; }
    .text-success { color: #198754; }
    .text-warning { color: #b58105; }
    .row { display: flex; flex-wrap: wrap; margin: -12px; }
    .row > div { padding: 12px; }
    .col-md-3, .col-xl-3 { width: 25%; }
    .col-md-6 { width: 50%; }
    .g-3, .g-4 { row-gap: 0; }
    .gap-1 { gap: 4px; }
    .card, .border {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
    }
    .card-body { padding: 24px; }
    .h-100 { height: 100%; }
    .shadow-sm { box-shadow: 0 2px 8px rgba(0, 0, 0, .08); }
    .border-primary { border-color: #0d6efd; }
    .border-success { border-color: #198754; }
    .border-warning { border-color: #ffc107; }
    .border-danger { border-color: #dc3545; }
    .rounded { border-radius: 8px; }
    .justify-content-between { justify-content: space-between; }
    .align-items-center { align-items: center; }
    .list-group-item {
        display: block;
        padding: 16px;
        background: white;
        border: 1px solid #dee2e6;
        color: #212529;
        text-decoration: none;
    }
    .table-responsive { overflow-x: auto; background: white; }
    .table { width: 100%; border-collapse: collapse; }
    .table th, .table td {
        padding: 12px;
        border-bottom: 1px solid #dee2e6;
        text-align: left;
    }
    .table-primary { background: #cfe2ff; }
    .text-end { text-align: right !important; }
    .btn {
        display: inline-block;
        padding: 8px 14px;
        border: 1px solid #6c757d;
        border-radius: 6px;
        text-decoration: none;
    }
    .badge {
        display: inline-block;
        padding: 6px 9px;
        border-radius: 6px;
    }
    .text-bg-success { background: #198754; color: white; }
    .text-bg-danger { background: #dc3545; color: white; }
    .text-bg-warning { background: #ffc107; color: #212529; }
    .alert { padding: 16px; border-radius: 8px; }
    .alert-info { background: #cff4fc; }
    @media (max-width: 768px) {
        .col-md-3, .col-md-6, .col-xl-3 { width: 100%; }
        .navbar .container { align-items: flex-start; }
        .navbar-nav { flex-wrap: wrap; }
    }
    """

    return f"""<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{safe_title}</title>
    <link href="{bootstrap}" rel="stylesheet">
    <style>{fallback_css}</style>
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand fw-semibold" href="/">HomeParty</a>
            <div class="navbar-nav flex-row flex-wrap gap-1">
                <a class="nav-link" href="/events/">События</a>
                <a class="nav-link" href="/participants/">Участники</a>
                <a class="nav-link" href="/tasks/">Задачи</a>
                <a class="nav-link" href="/expenses/">Расходы</a>
            </div>
        </div>
    </nav>
    <main class="container py-5">{content}</main>
</body>
</html>"""


def index(request) -> HttpResponse:
    """Показать главную страницу приложения."""
    events = load_events("data/events.json")
    participants = load_participants(
        "data/participants.json",
        events,
    )
    tasks = load_tasks("data/tasks.json", events)
    expenses = load_expenses("data/expenses.json", events)

    cards = (
        ("События", len(events), "/events/", "primary"),
        (
            "Участники",
            len(participants),
            "/participants/",
            "success",
        ),
        ("Задачи", len(tasks), "/tasks/", "warning"),
        ("Расходы", len(expenses), "/expenses/", "danger"),
    )

    card_html = "".join(
        f"""
        <div class="col-md-6 col-xl-3">
            <a class="text-decoration-none" href="{url}">
                <div class="card h-100 border-{color} shadow-sm">
                    <div class="card-body">
                        <h2 class="h5 text-{color}">{name}</h2>
                        <p class="display-6 mb-0 text-dark">{count}</p>
                    </div>
                </div>
            </a>
        </div>
        """
        for name, count, url, color in cards
    )

    content = f"""
    <section class="mb-5">
        <h1 class="display-4 fw-semibold">HomeParty</h1>
        <p class="lead">
            Веб-интерфейс сервиса организации домашних праздников.
        </p>
    </section>
    <section class="row g-4">{card_html}</section>
    """

    return HttpResponse(page("HomeParty", content))

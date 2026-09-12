from datetime import date


event_name = "День рождения"
event_date = date(2026, 10, 10)

participants_count = 12

budget = 18000
planned_expenses = 15000


def get_event_info(name, event_date):
    return f"Событие: {name}, дата: {event_date}"


def check_participants(count):
    if count <= 0:
        return "Участники не добавлены"

    if count <= 10:
        return "Небольшое количество участников"

    return "Большое количество участников"


def check_budget(budget, expenses):
    if expenses <= budget:
        return "Бюджета достаточно"

    return "Расходы превышают бюджет"


print(get_event_info(event_name, event_date))
print(f"Количество участников: {participants_count}")
print(check_participants(participants_count))
print(f"Бюджет: {budget} руб.")
print(f"Планируемые расходы: {planned_expenses} руб.")
print(check_budget(budget, planned_expenses))
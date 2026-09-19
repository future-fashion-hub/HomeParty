from datetime import date

from events import add_event, find_event, get_event_info, sort_events
from expenses import add_expense, check_budget, get_total_expenses
from models import Event
from participants import add_participant, count_participants
from storage import (
    find_event_by_id,
    load_events,
    load_expenses,
    load_participants,
    load_tasks,
    save_events,
    save_expenses,
    save_participants,
    save_tasks,
)
from tasks import add_task, complete_task, get_pending_tasks


EVENTS_FILE = "data/events.json"
PARTICIPANTS_FILE = "data/participants.json"
TASKS_FILE = "data/tasks.json"
EXPENSES_FILE = "data/expenses.json"


def show_menu() -> None:
    """Вывести главное меню приложения."""
    print("\n=== HomeParty ===")
    print("1. Показать события")
    print("2. Добавить событие")
    print("3. Найти событие")
    print("4. Добавить участника")
    print("5. Показать количество участников")
    print("6. Добавить задачу")
    print("7. Выполнить задачу")
    print("8. Показать невыполненные задачи")
    print("9. Добавить расход")
    print("10. Проверить бюджет")
    print("0. Выход")


def input_int(prompt: str) -> int:
    """Безопасно запросить целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Безопасно запросить число."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt)

        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            print(
                "Ошибка: используйте формат "
                "ГГГГ-ММ-ДД."
            )


def show_events(events: list[Event]) -> None:
    """Вывести список событий."""
    if not events:
        print("Событий пока нет.")
        return

    for event in sort_events(events):
        print(
            f"{event.id}. {event}"
        )


def get_event_from_user(
    events: list[Event],
) -> Event | None:
    """Получить событие по введённому ID."""
    event_id = input_int("ID события: ")

    event = find_event_by_id(
        events,
        event_id,
    )

    if event is None:
        print("Событие не найдено.")

    return event


def main() -> None:
    """Точка запуска приложения HomeParty."""
    events = load_events(EVENTS_FILE)

    participants = load_participants(
        PARTICIPANTS_FILE,
        events,
    )

    tasks = load_tasks(
        TASKS_FILE,
        events,
    )

    expenses = load_expenses(
        EXPENSES_FILE,
        events,
    )

    while True:
        show_menu()

        choice = input(
            "Выберите действие: "
        )

        if choice == "1":
            show_events(events)

        elif choice == "2":
            name = input(
                "Название события: "
            )

            event_date = input_date(
                "Дата события "
                "в формате ГГГГ-ММ-ДД: "
            )

            budget = input_float(
                "Бюджет: "
            )

            event = add_event(
                events,
                name,
                event_date,
                budget,
            )

            save_events(
                EVENTS_FILE,
                events,
            )

            print("Событие добавлено:")
            print(get_event_info(event))

        elif choice == "3":
            query = input(
                "Введите название события: "
            )

            found_events = find_event(
                events,
                query,
            )

            if not found_events:
                print("События не найдены.")
            else:
                for event in found_events:
                    print(
                        f"{event.id}. "
                        f"{get_event_info(event)}"
                    )

        elif choice == "4":
            event = get_event_from_user(
                events
            )

            if event is None:
                continue

            name = input(
                "Имя участника: "
            )

            participant = add_participant(
                participants,
                event,
                name,
            )

            save_participants(
                PARTICIPANTS_FILE,
                participants,
            )

            print(
                f"Участник "
                f"{participant.name} "
                f"добавлен."
            )

        elif choice == "5":
            event = get_event_from_user(
                events
            )

            if event is None:
                continue

            count = count_participants(
                participants,
                event,
            )

            print(
                f"Количество участников: "
                f"{count}"
            )

        elif choice == "6":
            event = get_event_from_user(
                events
            )

            if event is None:
                continue

            title = input(
                "Название задачи: "
            )

            task = add_task(
                tasks,
                event,
                title,
            )

            save_tasks(
                TASKS_FILE,
                tasks,
            )

            print(
                f"Задача "
                f"«{task.title}» "
                f"добавлена."
            )

        elif choice == "7":
            task_id = input_int(
                "ID задачи: "
            )

            if complete_task(
                tasks,
                task_id,
            ):
                save_tasks(
                    TASKS_FILE,
                    tasks,
                )

                print(
                    "Задача выполнена."
                )
            else:
                print(
                    "Задача не найдена."
                )

        elif choice == "8":
            event = get_event_from_user(
                events
            )

            if event is None:
                continue

            pending_tasks = get_pending_tasks(
                tasks,
                event,
            )

            if not pending_tasks:
                print(
                    "Невыполненных задач нет."
                )
            else:
                for task in pending_tasks:
                    print(
                        f"{task.id}. "
                        f"{task}"
                    )

        elif choice == "9":
            event = get_event_from_user(
                events
            )

            if event is None:
                continue

            title = input(
                "Название расхода: "
            )

            amount = input_float(
                "Сумма расхода: "
            )

            expense = add_expense(
                expenses,
                event,
                title,
                amount,
            )

            save_expenses(
                EXPENSES_FILE,
                expenses,
            )

            print(
                f"Расход "
                f"«{expense.title}» "
                f"добавлен."
            )

        elif choice == "10":
            event = get_event_from_user(
                events
            )

            if event is None:
                continue

            total = get_total_expenses(
                expenses,
                event,
            )

            print(
                f"Бюджет: "
                f"{event.budget} руб."
            )

            print(
                f"Расходы: "
                f"{total} руб."
            )

            print(
                check_budget(
                    event,
                    total,
                )
            )

        elif choice == "0":
            save_events(
                EVENTS_FILE,
                events,
            )

            save_participants(
                PARTICIPANTS_FILE,
                participants,
            )

            save_tasks(
                TASKS_FILE,
                tasks,
            )

            save_expenses(
                EXPENSES_FILE,
                expenses,
            )

            print(
                "Работа программы завершена."
            )
            break

        else:
            print(
                "Неизвестная команда."
            )


if __name__ == "__main__":
    main()

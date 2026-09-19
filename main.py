from datetime import date

from events import add_event, find_event, get_event_info, sort_events
from expenses import add_expense, check_budget, get_total_expenses
from participants import add_participant, count_participants
from storage import load_json, save_json
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


def input_date(prompt: str) -> date:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt)

        try:
            return date.fromisoformat(value)
        except ValueError:
            print("Ошибка: используйте формат ГГГГ-ММ-ДД.")


def show_events(events: list[dict]) -> None:
    """Вывести список событий."""
    if not events:
        print("Событий пока нет.")
        return

    for event in sort_events(events):
        print(
            f"{event['id']}. "
            f"{event['name']} | "
            f"{event['date']} | "
            f"бюджет: {event['budget']} руб."
        )


def main() -> None:
    """Точка запуска приложения HomeParty."""
    events = load_json(EVENTS_FILE)
    participants = load_json(PARTICIPANTS_FILE)
    tasks = load_json(TASKS_FILE)
    expenses = load_json(EXPENSES_FILE)

    while True:
        show_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            show_events(events)

        elif choice == "2":
            name = input("Название события: ")
            event_date = input_date(
                "Дата события в формате ГГГГ-ММ-ДД: "
            )
            budget = input_float("Бюджет: ")

            event = add_event(
                events,
                name,
                event_date,
                budget,
            )

            save_json(EVENTS_FILE, events)

            print("Событие добавлено:")
            print(get_event_info(event))

        elif choice == "3":
            query = input("Введите название события: ")

            found_events = find_event(
                events,
                query,
            )

            if not found_events:
                print("События не найдены.")
            else:
                for event in found_events:
                    print(get_event_info(event))

        elif choice == "4":
            event_id = input_int("ID события: ")
            name = input("Имя участника: ")

            participant = add_participant(
                participants,
                event_id,
                name,
            )

            save_json(
                PARTICIPANTS_FILE,
                participants,
            )

            print(
                f"Участник {participant['name']} добавлен."
            )

        elif choice == "5":
            event_id = input_int("ID события: ")

            count = count_participants(
                participants,
                event_id,
            )

            print(
                f"Количество участников: {count}"
            )

        elif choice == "6":
            event_id = input_int("ID события: ")
            title = input("Название задачи: ")

            task = add_task(
                tasks,
                event_id,
                title,
            )

            save_json(TASKS_FILE, tasks)

            print(
                f"Задача «{task['title']}» добавлена."
            )

        elif choice == "7":
            task_id = input_int("ID задачи: ")

            if complete_task(tasks, task_id):
                save_json(TASKS_FILE, tasks)
                print("Задача выполнена.")
            else:
                print("Задача не найдена.")

        elif choice == "8":
            event_id = input_int("ID события: ")

            pending_tasks = get_pending_tasks(
                tasks,
                event_id,
            )

            if not pending_tasks:
                print("Невыполненных задач нет.")
            else:
                for task in pending_tasks:
                    print(
                        f"{task['id']}. {task['title']}"
                    )

        elif choice == "9":
            event_id = input_int("ID события: ")
            title = input("Название расхода: ")
            amount = input_float("Сумма расхода: ")

            expense = add_expense(
                expenses,
                event_id,
                title,
                amount,
            )

            save_json(
                EXPENSES_FILE,
                expenses,
            )

            print(
                f"Расход «{expense['title']}» добавлен."
            )

        elif choice == "10":
            event_id = input_int("ID события: ")

            event = None

            for current_event in events:
                if current_event["id"] == event_id:
                    event = current_event
                    break

            if event is None:
                print("Событие не найдено.")
                continue

            total = get_total_expenses(
                expenses,
                event_id,
            )

            print(
                f"Бюджет: {event['budget']} руб."
            )
            print(
                f"Расходы: {total} руб."
            )
            print(
                check_budget(
                    event["budget"],
                    total,
                )
            )

        elif choice == "0":
            print("Работа программы завершена.")
            break

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()

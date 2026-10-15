-- name: events_list
-- Q01. Список событий: SELECT, сортировка.
SELECT id, name, date, budget FROM events ORDER BY date, id;

-- name: users_list
-- Q02. Список пользователей: SELECT, ORDER BY, LIMIT, OFFSET.
SELECT id, name, email FROM users ORDER BY name, id LIMIT 50 OFFSET 0;

-- name: events_by_budget
-- Q03. WHERE: события с бюджетом не меньше введённого значения.
SELECT id, name, date, budget FROM events
WHERE budget >= ? ORDER BY budget, id;

-- name: pending_tasks
-- Q04. WHERE: только незавершённые задачи (0 — в работе).
SELECT id, event_id, title, completed FROM tasks
WHERE completed = 0 ORDER BY event_id, id;

-- name: tasks_with_events
-- Q05. JOIN: все задачи с названием и датой события.
SELECT t.id, t.event_id, t.title, t.completed,
       e.name AS event_name, e.date AS event_date
FROM tasks AS t JOIN events AS e ON e.id = t.event_id ORDER BY t.id;

-- name: expenses_with_events
-- Q06. JOIN: расходы с названием события.
SELECT x.id, x.event_id, x.title, x.amount, e.name AS event_name
FROM expenses AS x JOIN events AS e ON e.id = x.event_id ORDER BY x.id;

-- name: overview
-- Q07. Агрегаты: количество записей всех сущностей, включая пустые таблицы.
SELECT (SELECT COUNT(*) FROM events) AS event_count,
       (SELECT COUNT(*) FROM participants) AS participant_count,
       (SELECT COUNT(*) FROM tasks) AS task_count,
       (SELECT COUNT(*) FROM expenses) AS expense_count,
       (SELECT COUNT(*) FROM users) AS user_count;

-- name: expense_totals
-- Q08. Агрегаты COUNT, SUM, AVG, MIN, MAX; COALESCE обрабатывает NULL.
SELECT COUNT(*) AS count, COALESCE(SUM(amount), 0) AS total,
       COALESCE(AVG(amount), 0) AS average,
       COALESCE(MIN(amount), 0) AS minimum,
       COALESCE(MAX(amount), 0) AS maximum FROM expenses;

-- name: tasks_by_event
-- Q09. GROUP BY и LEFT JOIN: задачи по событиям, в том числе без задач.
SELECT e.id, e.name, COUNT(t.id) AS task_count,
       SUM(CASE WHEN t.completed = 0 THEN 1 ELSE 0 END) AS pending_count
FROM events AS e LEFT JOIN tasks AS t ON t.event_id = e.id
GROUP BY e.id, e.name ORDER BY e.id;

-- name: expenses_by_event
-- Q10. GROUP BY: сумма расходов и остаток бюджета по событиям.
SELECT e.id, e.name, e.budget, COUNT(x.id) AS expense_count,
       COALESCE(SUM(x.amount), 0) AS spent,
       e.budget - COALESCE(SUM(x.amount), 0) AS remaining
FROM events AS e LEFT JOIN expenses AS x ON x.event_id = e.id
GROUP BY e.id, e.name, e.budget ORDER BY e.id;

-- name: busy_events
-- Q11. HAVING: события с числом открытых задач больше заданного порога.
SELECT e.id, e.name, COUNT(t.id) AS pending_count
FROM events AS e JOIN tasks AS t ON t.event_id = e.id
WHERE t.completed = 0
GROUP BY e.id, e.name HAVING COUNT(t.id) > ? ORDER BY e.id;

-- name: ready_events
-- Q12. Поиск по дате и NOT IN: события без незавершённых задач.
-- Аналог поиска свободного ресурса: готовность праздника к выбранной дате.
SELECT id, name, date, budget FROM events
WHERE date = ? AND id NOT IN (
    SELECT event_id FROM tasks WHERE completed = 0
) ORDER BY name, id;

-- name: event_detail
-- Q13. Параметризованный поиск одного события.
SELECT id, name, date, budget FROM events WHERE id = ?;

-- name: task_detail
-- Q14. JOIN и WHERE: отдельная задача и связанное событие.
SELECT t.id, t.event_id, t.title, t.completed,
       e.name AS event_name, e.date AS event_date
FROM tasks AS t JOIN events AS e ON e.id = t.event_id WHERE t.id = ?;

-- name: participants_with_events
-- Q15. JOIN: участники и названия событий.
SELECT p.id, p.event_id, p.name, e.name AS event_name
FROM participants AS p JOIN events AS e ON e.id = p.event_id ORDER BY p.id;

-- name: event_metrics
-- Q16. Агрегаты одного события без умножения строк несколькими JOIN.
SELECT (SELECT COUNT(*) FROM participants WHERE event_id = ?) AS participant_total,
       (SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE event_id = ?) AS spent;

-- name: event_pending_tasks
-- Q17. Задачи в работе для отдельного события.
SELECT id, event_id, title, completed FROM tasks
WHERE event_id = ? AND completed = 0 ORDER BY id;

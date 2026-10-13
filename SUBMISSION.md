# Готовый проект: StudyFlow

Ссылка для сдачи: https://github.com/Usmanovkairat/studyflow

Это простой локальный трекер заданий студента: предметы, задания, сроки, приоритеты, статусы, поиск и фильтры, статистика и CSV. Стек: Python Flask, SQLite, HTML/CSS. Без внешней базы, React, Docker и платных сервисов.

## Что показать преподавателю
1. README и работа приложения: создать предмет, добавить задание, поменять статус, применить фильтры и скачать CSV.
2. `chat-brainstorm.md`: честный журнал выбора идеи и подлинные выдержки из разговора, отдельно от AI-записи решений.
3. `AGENTS.md`, `AGENT.md`, `process.md`, `_docs/process.md`, роли в `_docs/team/` и `roles/`.
4. `_docs/plan.md`, архитектуру и шесть подробных спецификаций; реальные Issues: https://github.com/Usmanovkairat/studyflow/issues?q=is%3Aissue
5. Отчёты QA в `_docs/qa/`, включая проверку свежего публичного клона; 99 тестов прошли.
6. `_docs/publication.md`: настоящие коммиты и даты открытия/закрытия Issues.

## Запуск на Windows
Открой PowerShell в папке скачанного проекта:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/demo.py
.\.venv\Scripts\python.exe -m flask --app studyflow run
```

Открой http://127.0.0.1:5000. Для тестов: `.\.venv\Scripts\python.exe -m pytest -q`. Demo запускается только на пустой базе и не перезаписывает существующие данные.

## Честная хронология
Локальная разработка и независимые проверки выполнены до создания удалённых Issues. После разрешения пользователя созданы репозиторий и реальные Issues, опубликованы коммиты по функциям и повторно проверен свежий клон. Все удалённые события имеют текущие реальные даты. Видео было недоступно; использована полная статья и пример проекта.

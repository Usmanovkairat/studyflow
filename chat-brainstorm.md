# Chat history and brainstorming — StudyFlow

**Project:** StudyFlow — a simple student assignment tracker  
**Repository:** https://github.com/Usmanovkairat/studyflow  
**Date of this conversation:** 13 October 2026  
**Methodology:** https://aishippingblog.com/p/ai-native-development-specifications

## 1. What this record contains

This file documents the real conversation and the decisions used to define StudyFlow. Section 2 contains selected actual messages and exact excerpts from the user's assignment attachment. It is not a complete export of every message. Sections 3–8 organize the documented decisions into the article's idea → scope → specification → architecture → backlog → implementation → QA flow. Those sections are an AI-written explanation, not additional historical user messages.

The user explicitly authorized the assistant to choose an application and technology stack independently. Therefore, the assistant made the initial product decisions without inventing a question-and-answer conversation. Later, the user explicitly requested a simple project and authorized GitHub publication.

## 2. Actual conversation history — relevant excerpts

The messages below appear in their real relative order. Text introduced as an excerpt quotes only the relevant part of a longer message. The attached assignment is identified separately from messages typed directly by the user. No exact message time is invented.

### Message 1 — User: assignment attachment, before implementation

The user supplied an assignment with these exact requirements:

> Your mission is to **COMPLETE MY ENTIRE UNIVERSITY ASSIGNMENT FROM START TO FINISH**, not just explain how to do it.

> Choose a practical, simple, but complete web application suitable for a university project.

> You are authorized to choose the idea and technical stack independently.

The attachment required a real frontend and backend, persistent database storage, CRUD, 4–6 meaningful features, simple setup and automated tests. It also required the AI-native workflow, Markdown specifications, genuine brainstorming evidence and actual GitHub Issues.

The attachment explicitly stated:

> Clearly distinguish actual conversation history from AI-generated reconstruction. Do not invent messages and present them as a real historical conversation.

### Message 2 — Assistant: application and initial stack selection

Actual excerpt:

> В файле — инструкция выполнить проект целиком. Начинаю работу по ней. Выберу StudyFlow: приложение для студентов с предметами, заданиями, сроками, фильтрами и статистикой, на Python Flask и SQLite.

English summary: the assistant selected a student assignment tracker called StudyFlow. The proposed stack was Python Flask and SQLite.

### Message 3 — Assistant: define users and product boundaries

Actual message:

> Зафиксировал границы StudyFlow: приложение для одного студента, запуск на своём компьютере, данные сохраняются в SQLite. Подготовлю шесть спецификаций с проверяемыми критериями до написания кода. В `chat-brainstorm.md` честно отмечу, что идею и стек я выбрал по вашему разрешению.

English summary: the MVP serves one student on a local computer. Product scope and six checkable feature specifications come before application code.

### Message 4 — Assistant: choose a simple interface and setup

Actual message:

> В проекте будет обычный интерфейс с серверными HTML-страницами, без отдельной сборки фронтенда. Это сокращает настройку: установить зависимости Python и запустить приложение одной командой.

English summary: use server-rendered HTML and CSS to keep installation simple.

### Message 5 — User: clarify simplicity and GitHub delivery

Actual message typed directly by the user later in the conversation:

> сделай это задание полностью в githab и дай мне готовый к сдаче
> продвинутый проект не надо

English summary: complete the GitHub delivery and keep the project simple. This clarification occurred after local implementation; it confirms the existing small scope rather than being presented as an earlier brainstorming reply.

### Message 6 — User: authorize browser creation and supply deadline

Actual message:

> да разрешаю
> дедлайн через 1,5-2 часа

This answered the assistant's request to create a public repository through the browser because the GitHub connector did not expose repository creation.

### Message 7 — User: confirm GitHub sign-in

Actual message:

> все я входил в гитхаб

The assistant then verified the signed-in account, created the public repository and used the connected GitHub tools to publish the specifications, six Issues, feature commits and QA evidence.

### Message 8 — User: request this expanded brainstorming file

Actual message:

> - Submit chat-brainstrom.txt or .md on how you brainstormed app. Chat history. Must the same flow as in article.
>
> сделай этого chat-brainstorm.md

This file was expanded in response. Its expansion does not change the actual sequence of the earlier conversation.

## 3. Brainstorming: compare possible application ideas

**AI-written decision explanation, not a quoted user dialogue.** The following alternatives were recorded in the PM decision document during this execution.

| Idea | Problem it solves | MVP complexity | Decision |
|---|---|---|---|
| Student assignment tracker | Students lose track of assignments and deadlines across courses. | Two main entities; clear CRUD and date logic. | Selected. |
| Recipe and ingredient tracker | People need cooking ideas and want to reduce food waste. | Recipes, ingredients, quantities and matching add more relationships. | Not selected for this assignment. |
| Internship application tracker | Students need to organize internship applications. | Companies, contacts and application stages increase scope. | Not selected for this assignment. |

StudyFlow was selected because it is useful, easy to demonstrate, and small enough to complete and verify. It still demonstrates real frontend, backend and persistent database behavior.

## 4. Scope the product before code

**AI-written specification of the decisions.** These are product questions and their documented resolutions, not a fabricated historical question-and-answer transcript.

| Product question | Resolution | Basis |
|---|---|---|
| Who uses the app? | One student working on their own computer. | Assistant's documented scope decision under delegated authority. |
| What problem does it solve? | Keep assignments, deadlines and completion status in one place. | Selected student-tracker idea. |
| What does the student record? | Courses and assignments with title, course, due date, priority, status and notes. | Product plan and feature specifications. |
| How does the student find work? | Search title/notes and combine course, priority and status filters. | MVP scope. |
| What appears on the home page? | Total, unfinished, completed and overdue counts; five upcoming assignments. | Dashboard specification. |
| How does work leave the app? | Export the current filtered results as CSV. | Export specification. |
| Is an account required? | No. This is a single-user localhost application. | Scope decision to keep setup simple. |
| Where are records saved? | A persistent local SQLite database. | Assignment's storage requirement and chosen architecture. |

### Intended user journey

1. Open StudyFlow on the local computer.
2. Create a course.
3. Add an assignment with its due date and priority.
4. Check the dashboard or filter the assignment list.
5. Edit an assignment or mark it complete; reopen it if needed.
6. Export selected assignments when useful.

### MVP features

1. Create, list, rename and safely delete courses.
2. Create, read, edit and delete assignments.
3. Change assignment status between todo, in progress and done.
4. Search and combine filters.
5. View workload, overdue counts and upcoming deadlines.
6. Download a CSV export.

### Out of scope

Accounts, multiple users, collaboration, email reminders, recurring tasks, AI recommendations, cloud deployment, payments and a separate frontend build pipeline. The user asked for a simple project, so these features were not added.

## 5. Save the specification and choose the architecture

The product decisions were saved in `_docs/plan.md` before application implementation. `_docs/architecture.md` describes the browser → Flask → SQLite architecture, database tables and validation boundaries.

The initial assistant message selected the app and stack together under the user's explicit autonomy instruction. The article normally separates product brainstorming from later stack selection. The table below explains the chosen stack; it is not a claim that a new stack-selection conversation occurred.

| Component | Choice | Reason |
|---|---|---|
| Frontend | HTML, CSS and Jinja templates | Simple forms and navigation; no separate build step. |
| Backend | Python Flask | Small framework suitable for a local CRUD application. |
| Database | SQLite through Python sqlite3 | Persistent data without a separate database server. |
| Tests | pytest and Flask test client | Test requests, validation, database changes and date rules. |
| Repository | GitHub | Publish code, specifications, real Issues and QA evidence. |

The model has `courses` and `tasks`. Each task references an existing course. Deleting a course with tasks is rejected. Empty titles, invalid dates, unknown courses and invalid statuses are rejected. Past dates are allowed. Completed tasks are excluded from overdue and upcoming counts.

## 6. Turn the specification into a backlog

The PM prepared six groomed tasks using the reference Issue #17's four sections: **Goal**, **Acceptance criteria**, **Out of scope**, **Constraints**.

| Actual GitHub Issue | Task | Specification |
|---|---|---|
| [#1](https://github.com/Usmanovkairat/studyflow/issues/1) | Bootstrap persistent local application | `_docs/issues/01.md` |
| [#2](https://github.com/Usmanovkairat/studyflow/issues/2) | Create and manage courses | `_docs/issues/02.md` |
| [#3](https://github.com/Usmanovkairat/studyflow/issues/3) | Manage assignments and completion | `_docs/issues/03.md` |
| [#4](https://github.com/Usmanovkairat/studyflow/issues/4) | Search and combine task filters | `_docs/issues/04.md` |
| [#5](https://github.com/Usmanovkairat/studyflow/issues/5) | Show dashboard and upcoming work | `_docs/issues/05.md` |
| [#6](https://github.com/Usmanovkairat/studyflow/issues/6) | Export filtered CSV and verify delivery | `_docs/issues/06.md` |

Tasks depend on the earlier foundations and were implemented sequentially. Each specification contains observable behavior and test requirements.

## 7. Context, roles and verification loop

The repository contains `AGENTS.md`, `CLAUDE.md`, `_docs/process.md`, `_docs/task-template.md` and role instructions in `_docs/team/`. The assignment's compatibility paths `AGENT.md`, `process.md` and `roles/` are included too.

The actual working loop was:

1. PM writes the scope and grooms the task.
2. Software engineer implements the specified behavior and runs tests.
3. Independent QA checks the acceptance criteria.
4. A FAIL returns to the engineer for correction.
5. QA repeats the affected checks and records PASS.
6. The orchestrator records acceptance and continues with the next task.

QA found real defects, including malformed CSRF input, very large course IDs, Unicode course-name duplicates and CSV control-character handling. The engineer fixed them, and independent QA verified the fixes. `_docs/qa/` preserves both failures and successful retests.

Final evidence includes 99 passing tests, successful clean-environment installation, fresh public-clone verification and real desktop/mobile browser workflows. GitHub Actions also ran the tests successfully.

## 8. Actual publication chronology and methodology limits

The conceptual order was idea → scope → specifications → implementation → independent QA → GitHub delivery. However, GitHub repository creation was initially blocked by the available connector's capabilities. Local development and QA therefore happened before real GitHub Issues existed.

After the user authorized browser creation and signed in, the assistant published specifications, opened six real Issues, published the verified implementation in six feature commits, published QA evidence, and closed the Issues after acceptance. The Issues have actual current timestamps; no events were backdated.

The article's one-question-at-a-time brainstorming dialogue was not carried out in the original conversation: the user had delegated idea and stack choices instead. This file follows the article's decision stages while honestly recording that difference. It does not invent user answers to make the history look different.

The embedded video was unavailable. The full accessible article, reference repository and example Issue #17 informed the process. Exact remote commits and Issue timestamps are recorded in `_docs/publication.md`.

## 9. Final agreed scope

A simple, local student assignment tracker with six useful feature groups, real SQLite persistence, accessible server-rendered pages, automated tests, independent QA and a public GitHub repository. No advanced product features were added.

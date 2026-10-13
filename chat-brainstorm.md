# Genuine brainstorming and decision record
## Provenance
This is an AI-generated decision log from the current authorized assignment execution on 2026-10-13. It is not a verbatim chat transcript and does not invent user replies. The actual user attachment requests autonomous product selection, a working app, the article's workflow, real GitHub publication wherever capabilities permit, and honest evidence.
## Ideas considered in this execution
| Idea | Benefits | Cost/scope |
|---|---|---|
| Student assignment tracker | Relevant to university; clear CRUD; useful due-date logic | Small local relational model |
| Recipe inventory app | Useful daily problem; ingredient relationships | Quantity and recipe matching broaden scope |
| Internship tracker | Useful student workflow | Contacts, application stages and external listings complicate MVP |
## Decision
Select **StudyFlow**, a local student assignment tracker. The orchestrator delegated the PM specification to this PM agent before implementation. No user was asked to select an idea because the attachment explicitly grants independent choice.
## Target problem
A student needs to know what work is due, which assignments are overdue and which tasks are complete across courses. A single dashboard and searchable list make this concrete.
## Scope decisions
Persist courses and assignments in SQLite. Build course CRUD with safe restricted deletion, task CRUD and completion, combined search/filtering, dashboard date logic and CSV export. Use Python Flask, HTML/CSS and pytest. Keep all functionality server-side with accessible forms. Exclude accounts, sharing, email reminders and public hosting. This keeps six coherent implementation tasks feasible while still demonstrating frontend/backend/database integration.
## Architecture reasoning
Two tables model one-to-many courses/tasks. Foreign keys prevent orphaned assignments. Parameterized SQL, validation, escaping and CSRF protect local workflows. Dates use ISO strings and local calendar comparisons. QA will verify actual behavior independently after implementation.
## Final handoff
PM creates methodology documents and six detailed task specifications; software engineer implements in dependency order; QA verifies acceptance and returns defects for correction. GitHub publication was initially blocked by missing repository creation capability. After the user authorized browser creation and signed in, real repository and issue publication proceeded; `_docs/publication.md` records the actual chronology.

## Selected exact conversation excerpts
These are selected exact excerpts supplied from the current conversation, not a full transcript. The generated decision record above remains explicitly separate. No question/reply exchange is invented.

**User-provided assignment attachment:**
> You are authorized to choose the idea and technical stack independently.

> Clearly distinguish actual conversation history from AI-generated reconstruction. Do not invent messages and present them as a real historical conversation.

**Assistant's actual initial project-selection message:**
> В файле — инструкция выполнить проект целиком. Начинаю работу по ней. Выберу StudyFlow: приложение для студентов с предметами, заданиями, сроками, фильтрами и статистикой, на Python Flask и SQLite.

## Later genuine user instructions
The user wrote: “сделай это задание полностью в githab и дай мне готовый к сдаче / продвинутый проект не надо”. The user then authorized browser repository creation and stated: “да разрешаю / дедлайн через 1,5-2 часа”. These selected excerpts explain keeping the product simple and using browser creation plus connected GitHub tools for publication.

# Product plan: StudyFlow
## Problem and user
University students track work across several courses and need one clear view of outstanding assignments. StudyFlow helps one student record, organize and complete their work on a local computer. The user authorized autonomous choice of product and technology.
## MVP scope
1. Persistent SQLite storage and a usable responsive Flask application.
2. Courses: create, list, rename and delete; deletion is rejected while tasks use the course.
3. Tasks: create, list, view, edit, delete and toggle completion. Fields: title, course, due date, priority, status and notes.
4. Case-insensitive text search and combined course, priority and status filters.
5. Dashboard totals, open/done/overdue counts and a due-date-ordered upcoming list.
6. CSV export of the current filtered task list and complete delivery documentation.
## Product rules
Course name is required, trimmed, at most 100 characters and case-insensitively unique. Task title is required, trimmed, at most 200 characters. Notes are optional and at most 5000 characters. Course must exist. Due date must be a real ISO calendar date (YYYY-MM-DD); past dates are permitted. Priority is low, medium or high; status is todo, in_progress or done. Defaults are medium and todo. Overdue means due date before today's local date and status other than done. Upcoming means unfinished tasks due today or later; show the earliest five, tie-break by task ID. Counts cover all tasks, independently of list filters.
## Acceptance and exclusions
All six issue specifications must pass automated and appropriate browser checks. Data survives restart. There is no authentication, collaboration, reminder scheduling, external API, mobile client or public deployment. Bind localhost by default. The user later supplied a relative deadline; use the conservative inferred cutoff in publication.md and report actual GitHub timestamps rather than inventing professor dates.
## Delivery
Provide source, requirements, setup instructions, actual QA evidence, brainstorming decisions, methodology files and six issue specifications. The public GitHub repository and actual issues are recorded in publication.md; track real remote events separately from the earlier local implementation.

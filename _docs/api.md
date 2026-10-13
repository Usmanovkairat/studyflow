# HTTP route contract
The MVP uses HTML form routes rather than a JSON API. GET requests never mutate data. All POST requests require CSRF tokens. Successful mutation redirects to a relevant list/detail page. Validation returns a rendered form with errors (400 or 422). Missing objects return 404; restricted course deletion returns 400 or 409 with a visible explanation.

| Method | Route | Behavior |
|---|---|---|
| GET | `/` | Dashboard, all-task counts, first five upcoming unfinished tasks |
| GET | `/courses` | List courses |
| GET/POST | `/courses/new` | Create course |
| GET/POST | `/courses/<id>/edit` | Rename course |
| POST | `/courses/<id>/delete` | Delete only unused course |
| GET | `/tasks` | List/filter tasks |
| GET/POST | `/tasks/new` | Create task |
| GET | `/tasks/<id>` | Read task details |
| GET/POST | `/tasks/<id>/edit` | Edit all task fields |
| POST | `/tasks/<id>/delete` | Delete task |
| POST | `/tasks/<id>/toggle` | done → todo, any unfinished status → done |
| GET | `/tasks/export.csv` | Export the filtered result as a CSV attachment |

Task list/export share query parameters `q`, `course_id`, `priority`, `status`. Search matches title and notes case-insensitively. All supplied filters combine with AND. Invalid enum/course filters return a helpful 400 response. Default ordering is due_date ascending, id ascending. Export columns: id, title, course, due_date, priority, status, notes. Encode UTF-8; use standard CSV quoting. Prefix values whose first effective character is =, +, -, @, tab or carriage return with an apostrophe to prevent spreadsheet formula execution.

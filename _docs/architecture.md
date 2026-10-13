# Architecture
## Components
Browser → Flask server-rendered templates → SQLite database. Python's sqlite3 keeps the stack small; pytest exercises real Flask requests and isolated databases. CSS provides a responsive interface; JavaScript may enhance forms but core flows work server-side.
## Data model
`courses`: id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE (case-insensitive comparison), created_at timestamp.
`tasks`: id INTEGER PRIMARY KEY, title TEXT NOT NULL, course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE RESTRICT, due_date ISO date TEXT NOT NULL, priority TEXT NOT NULL, status TEXT NOT NULL, notes TEXT NOT NULL DEFAULT '', created_at and updated_at timestamps. Enable foreign keys on every connection. Enforce enum constraints in schema and validate values at request boundaries. Index course_id and due_date where useful.
## Boundaries
Application factory supports isolated test configuration. One connection per request is closed on teardown. Mutations use transactions; failures roll back. Unknown IDs return 404. Invalid form input returns a helpful validation response and does not write data. Database location belongs in instance/ and must be ignored by git. Secret key comes from configuration/environment, with a local development fallback only. Protect all mutation routes with session CSRF tokens; tests cover missing/invalid tokens. HTML templates autoescape user content. SQL values always use parameters; filter/sort clauses come from allowlisted code.
## Deployment
Development server binds 127.0.0.1. This MVP is for trusted local use; network hosting and multi-user account isolation are out of scope. Backups can copy the database while the app is stopped.

# Decision log
- 2026-10-13: Choose StudyFlow student assignment tracking because it fits a university demonstration and has meaningful CRUD and time-based behavior.
- Use Flask, server-rendered HTML, SQLite and pytest to minimize build tooling while retaining a real backend and persistent storage.
- No authentication: one local user and localhost binding define the product boundary. Public deployment is excluded.
- Keep course deletion restrictive to prevent accidental loss of linked tasks.
- Use explicit status and priority enums; permit past due dates so students can record existing overdue assignments.
- Share filter semantics between list and CSV so export matches what the student sees.
- Preserve the article's `_docs/team` role structure; root aliases cover assignment-specified filenames.
- Keep honest local/remote distinction. Repository publication and actual issue creation cannot be claimed until verified; deadline is unknown.

# Testing guidelines
Use pytest with Flask test client and a separate temporary SQLite database for every test. Never use the student's real data. Test behaviors across request, persistence and rendered output boundaries rather than reproducing implementation logic.

Required coverage: valid and invalid course CRUD, case-insensitive uniqueness, restricted delete; task CRUD and completion transitions; invalid title/course/date/enums/notes; nonexistent IDs; combined filters and case-insensitive search; stable due date order; dashboard boundary dates and done exclusions; CSV header, escaping, filter parity and spreadsheet formula protection; CSRF rejection and HTML escaping; data remains available from a fresh application instance using the same database.

Freeze or inject today's date for deterministic overdue/upcoming tests where possible. Verify dashboard cards and task forms through browser or rendered-page inspection, including mobile viewport, empty states, errors, keyboard labels and readable focus. Record commands, actual counts and outcomes in QA evidence. Never pre-mark tests as passed. A failed test blocks the associated done criteria until fixed and rerun.

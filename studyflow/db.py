import sqlite3
from flask import current_app, g

SCHEMA = '''
CREATE TABLE IF NOT EXISTS courses (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL COLLATE NOCASE UNIQUE,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS tasks (
 id INTEGER PRIMARY KEY, title TEXT NOT NULL,
 course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
 due_date TEXT NOT NULL,
 priority TEXT NOT NULL CHECK(priority IN ('low','medium','high')),
 status TEXT NOT NULL CHECK(status IN ('todo','in_progress','done')),
 notes TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_tasks_course ON tasks(course_id);
CREATE INDEX IF NOT EXISTS idx_tasks_due ON tasks(due_date);
'''

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        # SQLite's built-in NOCASE only covers ASCII. Register the same
        # collation for schema uniqueness, ordering and comparisons.
        def unicode_nocase(left, right):
            left, right = left.casefold(), right.casefold()
            return (left > right) - (left < right)
        g.db.create_collation('NOCASE', unicode_nocase)
        g.db.create_function('CASEFOLD', 1, lambda value: value.casefold(), deterministic=True)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    get_db().executescript(SCHEMA)

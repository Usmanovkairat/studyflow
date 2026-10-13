"""Populate an empty development database; never overwrite existing student records."""
import sys
from pathlib import Path
from datetime import date, timedelta
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from studyflow import create_app
from studyflow.db import get_db


def main():
    app = create_app()
    with app.app_context():
        db = get_db()
        if db.execute('SELECT COUNT(*) FROM courses').fetchone()[0] or db.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]:
            raise SystemExit('Demo refused: database already contains records. Use a separate empty checkout.')
        with db:
            db.executemany('INSERT INTO courses(name) VALUES(?)', [('Information Systems',), ('Web Fundamentals',), ('Linear Algebra',)])
            today = date.today()
            rows = [
                ('Review the lecture',1,-1,'high','todo','Summarize the key definitions.'),
                ('Build a responsive page',2,0,'high','in_progress','Check keyboard focus and mobile layout.'),
                ('Practice matrix problems',3,2,'medium','todo','Complete exercises 1–5.'),
                ('Submit project outline',1,3,'low','done','Outline submitted.'),
                ('Prepare quiz notes',2,4,'medium','todo','Review HTML forms and CSS.'),
            ]
            db.executemany('INSERT INTO tasks(title,course_id,due_date,priority,status,notes) VALUES(?,?,?,?,?,?)',
                           [(title, course, (today+timedelta(days=offset)).isoformat(), priority,status,notes) for title,course,offset,priority,status,notes in rows])
    print('Demo created: 3 courses, 5 assignments. Restarting preserves them.')

if __name__ == '__main__':
    main()

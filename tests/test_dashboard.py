from datetime import date
from studyflow.db import get_db


def test_empty_counts(client):
    text = client.get('/').get_data(as_text=True)
    assert text.count('<strong>0</strong>') == 4
    assert 'Create your first course' in text


def test_boundary_counts_and_upcoming(app, client):
    app.config['TODAY_PROVIDER'] = lambda: date(2026, 10, 13)
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO courses(name) VALUES(?)', ('Math',))
        rows = []
        for day in ['2026-10-12','2026-10-13','2026-10-14']:
            for status in ['todo','in_progress','done']:
                rows.append((day+' '+status,1,day,'medium',status,''))
        rows += [('Extra '+str(i),1,'2026-10-14','high','todo','') for i in range(4)]
        db.executemany('INSERT INTO tasks(title,course_id,due_date,priority,status,notes) VALUES(?,?,?,?,?,?)', rows)
        db.commit()
    text = client.get('/').get_data(as_text=True)
    for label, count in [('Total assignments',13), ('Open assignments',10), ('Completed',3), ('Overdue',2)]:
        assert f'<p>{label}</p><strong>{count}</strong>' in text
    assert '2026-10-12 todo' not in text
    assert '2026-10-13 done' not in text
    titles = ['2026-10-13 todo','2026-10-13 in_progress','2026-10-14 todo','2026-10-14 in_progress','Extra 0']
    positions = [text.index('>'+title+'</a>') for title in titles]
    assert positions == sorted(positions)
    assert '>Extra 1</a>' not in text
    assert 'Math' in text and 'High priority' in text
    filtered = client.get('/?q=missing&status=done').get_data(as_text=True)
    assert '<p>Total assignments</p><strong>13</strong>' in filtered


def test_overdue_only_guidance_and_completion_updates(app, client, token):
    app.config['TODAY_PROVIDER'] = lambda: date(2026, 10, 13)
    with app.app_context():
        db=get_db()
        db.execute('INSERT INTO courses(name) VALUES(?)',('Math',))
        db.execute('INSERT INTO tasks(title,course_id,due_date,priority,status) VALUES(?,?,?,?,?)',('Old task',1,'2026-10-12','low','todo'))
        db.commit()
    assert b'No upcoming assignments' in client.get('/').data
    client.post('/tasks/1/toggle',data={'csrf_token':token})
    text=client.get('/').get_data(as_text=True)
    assert '<p>Completed</p><strong>1</strong>' in text
    assert '<p>Overdue</p><strong>0</strong>' in text

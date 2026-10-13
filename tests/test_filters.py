import pytest
from studyflow.db import get_db

@pytest.fixture
def seeded(app):
    with app.app_context():
        db = get_db()
        db.executemany('INSERT INTO courses(name) VALUES(?)', [('Math',), ('Science',)])
        db.executemany('INSERT INTO tasks(title,course_id,due_date,priority,status,notes) VALUES(?,?,?,?,?,?)', [
            ('МАТЕМАТИКА',1,'2026-10-15','high','todo','algebra'),
            ('Other',2,'2026-10-14','high','todo','математика details'),
            ('Literal 100%_done',1,'2026-10-14','low','done',''),
            ('Fourth',1,'2026-10-14','high','in_progress','STRASSE'),
        ])
        db.commit()

def test_combined_search_order_and_controls(app, client, seeded):
    response = client.get('/tasks?q=математика&course_id=1&priority=high&status=todo')
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert 'МАТЕМАТИКА' in text and '>Other</a>' not in text
    assert 'value="1" selected' in text and 'value="high" selected' in text
    assert 'value="todo" selected' in text and 'value="математика"' in text
    content = client.get('/tasks').get_data(as_text=True)
    assert content.index('>Other</a>') < content.index('>Literal 100%_done</a>') < content.index('>Fourth</a>') < content.index('>МАТЕМАТИКА</a>')

@pytest.mark.parametrize('query, expected', [('q=ALgeBra', 'МАТЕМАТИКА'),('q=straße','Fourth'),('q=%25_', 'Literal 100%_done')])
def test_unicode_notes_literal_substrings(client, seeded, query, expected):
    text = client.get('/tasks?' + query).get_data(as_text=True)
    assert expected in text and '1 assignment shown' in text

@pytest.mark.parametrize('query', ['priority=bad','status=bad','course_id=99','course_id=oops','course_id='+'9'*100])
def test_invalid_filters_helpful(client, seeded, query):
    response = client.get('/tasks?' + query)
    assert response.status_code == 400
    assert b'filter' in response.data

def test_no_match_clear_and_no_mutation(app, client, seeded):
    assert b'No matching assignments' in client.get('/tasks?q=missing').data
    assert b'4 assignments shown' in client.get('/tasks').data
    with app.app_context():
        assert get_db().execute('SELECT COUNT(*) FROM tasks').fetchone()[0] == 4

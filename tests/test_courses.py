import pytest
from studyflow.db import get_db


def create(client, token, name='Calculus'):
    return client.post('/courses/new', data={'name': name, 'csrf_token': token})

def test_course_lifecycle(app, client, token):
    assert b'No courses yet' in client.get('/courses').data
    assert create(client, token, '  Calculus  ').status_code == 302
    assert b'Calculus' in client.get('/courses').data
    assert b'Confirm delete' in client.get('/courses').data
    assert client.get('/courses/1/edit').status_code == 200
    assert client.post('/courses/1/edit', data={'name': 'Algebra', 'csrf_token': token}).status_code == 302
    with app.app_context():
        assert get_db().execute('SELECT name FROM courses').fetchone()['name'] == 'Algebra'
    assert client.post('/courses/1/delete', data={'csrf_token': token}).status_code == 302
    assert b'No courses yet' in client.get('/courses').data

@pytest.mark.parametrize('name', ['', '  ', 'x' * 101])
def test_invalid_course_has_no_write(app, client, token, name):
    response = create(client, token, name)
    assert response.status_code == 400
    assert b'between 1 and 100' in response.data
    with app.app_context():
        assert get_db().execute('SELECT COUNT(*) FROM courses').fetchone()[0] == 0

def test_duplicate_create_and_edit_preserve_data(app, client, token):
    create(client, token, 'Math')
    create(client, token, 'Physics')
    assert create(client, token, 'mAtH').status_code == 400
    response = client.post('/courses/2/edit', data={'name': 'MATH', 'csrf_token': token})
    assert response.status_code == 400
    assert b'value="MATH"' in response.data
    with app.app_context():
        assert [row['name'] for row in get_db().execute('SELECT name FROM courses ORDER BY id')] == ['Math', 'Physics']
    assert client.post('/courses/1/edit', data={'name': 'math', 'csrf_token': token}).status_code == 302

def test_referenced_course_cannot_delete(app, client, token):
    create(client, token)
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO tasks(title,course_id,due_date,priority,status) VALUES(?,?,?,?,?)', ('Homework', 1, '2026-10-13', 'medium', 'todo'))
        db.commit()
    response = client.post('/courses/1/delete', data={'csrf_token': token})
    assert response.status_code == 409
    assert b'Delete or move' in response.data
    with app.app_context():
        assert get_db().execute('SELECT COUNT(*) FROM courses').fetchone()[0] == 1
        assert get_db().execute('SELECT COUNT(*) FROM tasks').fetchone()[0] == 1

@pytest.mark.parametrize('course_id', ['999', '9' * 100])
def test_missing_course(app, client, token, course_id):
    assert client.get(f'/courses/{course_id}/edit').status_code == 404
    for action in ['edit', 'delete']:
        assert client.post(f'/courses/{course_id}/{action}', data={'csrf_token': token, 'name': 'Test'}).status_code == 404

def test_course_csrf_and_escape(app, client, token):
    assert client.post('/courses/new', data={'name': 'Bad'}).status_code == 400
    create(client, token, '<script>alert(1)</script>')
    response = client.get('/courses')
    assert b'&lt;script&gt;' in response.data
    assert b'<script>' not in response.data
    for action in ['edit', 'delete']:
        assert client.post('/courses/1/' + action, data={'csrf_token': 'wrong', 'name': 'Bad'}).status_code == 400
    assert client.get('/courses/1/delete').status_code == 405


@pytest.mark.parametrize('original,duplicate', [('Математика', 'МАТЕМАТИКА'), ('Straße', 'STRASSE'), ('Ақпарат', 'АҚПАРАТ')])
def test_unicode_casefold_uniqueness(app, client, token, original, duplicate):
    import sqlite3
    assert create(client, token, original).status_code == 302
    assert create(client, token, duplicate).status_code == 400
    assert create(client, token, 'Other course').status_code == 302
    assert client.post('/courses/2/edit', data={'name': duplicate, 'csrf_token': token}).status_code == 400
    assert client.post('/courses/1/edit', data={'name': duplicate, 'csrf_token': token}).status_code == 302
    with app.app_context():
        db = get_db()
        with pytest.raises(sqlite3.IntegrityError):
            db.execute('INSERT INTO courses(name) VALUES (?)', (original,))
        db.rollback()
        assert db.execute('SELECT COUNT(*) FROM courses').fetchone()[0] == 2

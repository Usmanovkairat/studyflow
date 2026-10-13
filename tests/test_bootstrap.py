import sqlite3
import pytest
from flask import g, render_template_string
from studyflow import create_app
from studyflow.db import get_db
from studyflow.validation import validate_course, validate_task

def test_home_accessible(client):
    response = client.get('/')
    assert response.status_code == 200
    for expected in (b'lang="en"', b'Skip to content', b'Main navigation', b'A fresh start'):
        assert expected in response.data

def test_persistence_and_foreign_keys(app):
    with app.app_context():
        db = get_db()
        assert db.execute('PRAGMA foreign_keys').fetchone()[0] == 1
        db.execute('INSERT INTO courses(name) VALUES (?)', ('Calculus',))
        db.commit()
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("INSERT INTO tasks(title,course_id,due_date,priority,status) VALUES (?,?,?,?,?)", ('A', 99, '2026-10-13', 'medium', 'todo'))
        db.rollback()
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute('SELECT 1')
    second = create_app({'TESTING': True, 'DATABASE': app.config['DATABASE'], 'SECRET_KEY': 'other'})
    with second.app_context():
        assert get_db().execute('SELECT name FROM courses').fetchone()['name'] == 'Calculus'

def test_csrf_rejects_missing_invalid_accepts_valid(app, client):
    @app.post('/test-mutation')
    def mutation():
        return 'accepted'
    client.get('/')
    with client.session_transaction() as session:
        session['csrf_token'] = 'test-token'
    token = 'test-token'
    assert client.post('/test-mutation').status_code == 400
    assert client.post('/test-mutation', data={'csrf_token': 'wrong'}).status_code == 400
    assert client.post('/test-mutation', data={'csrf_token': '错误'}).status_code == 400
    assert client.post('/test-mutation', data={'csrf_token': token}).status_code == 200

def test_validation_and_escape(app):
    assert validate_course({'name': '  Math  '}) == ({'name': 'Math'}, {})
    assert 'name' in validate_course({'name': ' '})[1]
    with app.app_context():
        db = get_db()
        values, errors = validate_task({'title': ' ', 'course_id': '1', 'due_date': '2026-02-30', 'priority': 'urgent', 'status': 'unknown', 'notes': 'x' * 5001}, db)
        assert set(errors) == {'title', 'course_id', 'due_date', 'priority', 'status', 'notes'}
        assert render_template_string('{{ value }}', value='<script>alert(1)</script>') == '&lt;script&gt;alert(1)&lt;/script&gt;'

def test_production_requires_secret(tmp_path, monkeypatch):
    monkeypatch.setenv('STUDYFLOW_ENV', 'production')
    monkeypatch.delenv('STUDYFLOW_SECRET_KEY', raising=False)
    with pytest.raises(RuntimeError, match='STUDYFLOW_SECRET_KEY'):
        create_app({'DATABASE': str(tmp_path / 'prod.sqlite')})


def test_oversized_course_id_is_validation_error(app):
    with app.app_context():
        values, errors = validate_task({'title': 'Homework', 'course_id': '9' * 100, 'due_date': '2026-10-13'}, get_db())
        assert errors == {'course_id': 'Select an existing course.'}

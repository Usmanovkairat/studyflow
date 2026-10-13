import pytest
from studyflow.db import get_db
from studyflow import create_app

@pytest.fixture
def task_data(client, token):
    client.post('/courses/new', data={'name': 'Math', 'csrf_token': token})
    return {'title': '  Homework  ', 'course_id': '1', 'due_date': '2020-02-29', 'notes': 'Line one\nLine two', 'csrf_token': token}

def test_task_lifecycle(app, client, token, task_data):
    assert b'No assignments yet' in client.get('/tasks').data
    assert client.get('/tasks/new').status_code == 200
    assert client.post('/tasks/new', data=task_data).status_code == 302
    response = client.get('/tasks/1')
    assert response.status_code == 200
    assert b'Overdue' in response.data and b'Confirm delete' in response.data
    with app.app_context():
        task = get_db().execute('SELECT * FROM tasks').fetchone()
        assert task['title'] == 'Homework'
        assert (task['priority'], task['status']) == ('medium', 'todo')
    assert client.get('/tasks/1/edit').status_code == 200
    edited = dict(task_data, title='Updated', status='in_progress', priority='high', notes=' New notes ')
    assert client.post('/tasks/1/edit', data=edited).status_code == 302
    for expected in ('done', 'todo'):
        assert client.post('/tasks/1/toggle', data={'csrf_token': token}).status_code == 302
        with app.app_context():
            assert get_db().execute('SELECT status FROM tasks').fetchone()[0] == expected
        if expected == 'done':
            assert b'Overdue' not in client.get('/tasks/1').data
    second = create_app({'TESTING': True, 'DATABASE': app.config['DATABASE'], 'SECRET_KEY': 'test'})
    assert b'Updated' in second.test_client().get('/tasks/1').data
    assert client.post('/tasks/1/delete', data={'csrf_token': token}).status_code == 302
    assert client.get('/tasks/1').status_code == 404

@pytest.mark.parametrize('field,value', [('title',''),('title',' '),('title','x'*201),('notes','x'*5001),('notes',' '*5001),('course_id',''),('course_id','99'),('course_id','9'*100),('due_date',''),('due_date','2026-02-29'),('due_date','20261013'),('due_date','2026-1-1'),('priority','urgent'),('status','complete')])
def test_invalid_task_create_edit(app, client, token, task_data, field, value):
    invalid = dict(task_data, **{field: value})
    assert client.post('/tasks/new', data=invalid).status_code == 400
    with app.app_context():
        assert get_db().execute('SELECT COUNT(*) FROM tasks').fetchone()[0] == 0
    client.post('/tasks/new', data=task_data)
    assert client.post('/tasks/1/edit', data=invalid).status_code == 400
    with app.app_context():
        assert get_db().execute('SELECT title FROM tasks').fetchone()[0] == 'Homework'

def test_boundaries_and_escape(app, client, token, task_data):
    valid = dict(task_data, title='x'*200, notes='x'*5000)
    assert client.post('/tasks/new', data=valid).status_code == 302
    bad_html = dict(task_data, title='<script>Title</script>', notes='<img src=x onerror=alert(1)>')
    assert client.post('/tasks/new', data=bad_html).status_code == 302
    for path in ['/tasks', '/tasks/2', '/tasks/2/edit']:
        content = client.get(path).data
        assert b'&lt;script&gt;' in content and b'<script>' not in content
    assert b'&lt;img' in client.get('/tasks/2').data

def test_no_courses_and_mutation_security(client, token):
    assert b'Add a course first' in client.get('/tasks/new').data
    assert client.post('/tasks/new', data={'title':'test'}).status_code == 400
    for task_id in ['999', '9'*100]:
        assert client.get('/tasks/'+task_id).status_code == 404
        assert client.get('/tasks/'+task_id+'/edit').status_code == 404
        for action in ['edit', 'delete', 'toggle']:
            assert client.post('/tasks/'+task_id+'/'+action, data={'csrf_token':token}).status_code == 404
            assert client.post('/tasks/'+task_id+'/'+action, data={'csrf_token':'bad'}).status_code == 400
    assert client.get('/tasks/1/delete').status_code == 405
    assert client.get('/tasks/1/toggle').status_code == 405

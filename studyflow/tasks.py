from datetime import date
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from .db import get_db
from .validation import PRIORITIES, STATUSES, validate_task

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def find_task(task_id):
    if task_id > 9223372036854775807:
        abort(404, description='Assignment not found.')
    task = get_db().execute('SELECT t.*, c.name AS course_name FROM tasks t JOIN courses c ON c.id = t.course_id WHERE t.id = ?', (task_id,)).fetchone()
    if task is None:
        abort(404, description='Assignment not found.')
    return task

@bp.get('')
def index():
    tasks = get_db().execute('SELECT t.*, c.name AS course_name FROM tasks t JOIN courses c ON c.id = t.course_id ORDER BY t.due_date, t.id').fetchall()
    return render_template('tasks/index.html', tasks=tasks, today=date.today().isoformat())

@bp.route('/new', methods=['GET', 'POST'])
def new():
    return task_form()

@bp.get('/<int:task_id>')
def detail(task_id):
    return render_template('tasks/detail.html', task=find_task(task_id), today=date.today().isoformat())

@bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
def edit(task_id):
    return task_form(find_task(task_id))

def task_form(task=None):
    db = get_db()
    courses = db.execute('SELECT * FROM courses ORDER BY name COLLATE NOCASE, id').fetchall()
    values = dict(task) if task else {'title': '', 'course_id': '', 'due_date': '', 'priority': 'medium', 'status': 'todo', 'notes': ''}
    errors = {}
    if request.method == 'POST':
        values, errors = validate_task(request.form, db)
        if not errors:
            params = tuple(values[key] for key in ('title', 'course_id', 'due_date', 'priority', 'status', 'notes'))
            with db:
                if task:
                    db.execute('UPDATE tasks SET title=?,course_id=?,due_date=?,priority=?,status=?,notes=?,updated_at=CURRENT_TIMESTAMP WHERE id=?', params + (task['id'],))
                    task_id = task['id']
                else:
                    task_id = db.execute('INSERT INTO tasks(title,course_id,due_date,priority,status,notes) VALUES(?,?,?,?,?,?)', params).lastrowid
            flash('Assignment updated.' if task else 'Assignment created.')
            return redirect(url_for('tasks.detail', task_id=task_id))
    return render_template('tasks/form.html', task=task, courses=courses, values=values, errors=errors, priorities=PRIORITIES, statuses=STATUSES), 400 if errors else 200

@bp.post('/<int:task_id>/delete')
def delete(task_id):
    find_task(task_id)
    with get_db() as db:
        db.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    flash('Assignment deleted.')
    return redirect(url_for('tasks.index'))

@bp.post('/<int:task_id>/toggle')
def toggle(task_id):
    task = find_task(task_id)
    status = 'todo' if task['status'] == 'done' else 'done'
    with get_db() as db:
        db.execute('UPDATE tasks SET status=?,updated_at=CURRENT_TIMESTAMP WHERE id=?', (status, task_id))
    flash('Assignment reopened.' if status == 'todo' else 'Assignment completed.')
    return redirect(url_for('tasks.detail', task_id=task_id))

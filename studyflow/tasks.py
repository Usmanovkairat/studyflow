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

def filtered_tasks(args):
    db = get_db()
    filters = {key: args.get(key, '').strip() for key in ('q', 'course_id', 'priority', 'status')}
    clauses, params = [], []
    if filters['q']:
        clauses.append('(instr(CASEFOLD(t.title), ?) > 0 OR instr(CASEFOLD(t.notes), ?) > 0)')
        params.extend([filters['q'].casefold()] * 2)
    for key, allowed in (('priority', PRIORITIES), ('status', STATUSES)):
        if filters[key]:
            if filters[key] not in allowed:
                abort(400, description='Select a valid ' + key + ' filter.')
            clauses.append('t.' + key + ' = ?')
            params.append(filters[key])
    if filters['course_id']:
        try:
            course_id = int(filters['course_id'])
            if not db.execute('SELECT id FROM courses WHERE id=?', (course_id,)).fetchone():
                raise ValueError
        except (ValueError, OverflowError):
            abort(400, description='Select an existing course for the course filter.')
        clauses.append('t.course_id = ?')
        params.append(course_id)
    sql = 'SELECT t.*, c.name AS course_name FROM tasks t JOIN courses c ON c.id = t.course_id'
    if clauses:
        sql += ' WHERE ' + ' AND '.join(clauses)
    return db.execute(sql + ' ORDER BY t.due_date, t.id', params).fetchall(), filters

@bp.get('')
def index():
    tasks, filters = filtered_tasks(request.args)
    courses = get_db().execute('SELECT * FROM courses ORDER BY name COLLATE NOCASE, id').fetchall()
    return render_template('tasks/index.html', tasks=tasks, filters=filters, courses=courses,
                           priorities=PRIORITIES, statuses=STATUSES, today=date.today().isoformat())

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

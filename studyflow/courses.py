import sqlite3
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from .db import get_db
from .validation import validate_course

bp = Blueprint('courses', __name__, url_prefix='/courses')

def find_course(course_id):
    if course_id > 9223372036854775807:
        abort(404, description='Course not found.')
    course = get_db().execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    if course is None:
        abort(404, description='Course not found.')
    return course

@bp.get('')
def index():
    courses = get_db().execute('SELECT c.*, COUNT(t.id) AS task_count FROM courses c LEFT JOIN tasks t ON t.course_id = c.id GROUP BY c.id ORDER BY c.name COLLATE NOCASE, c.id').fetchall()
    return render_template('courses/index.html', courses=courses)

@bp.route('/new', methods=['GET', 'POST'])
def new():
    return course_form()

@bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
def edit(course_id):
    return course_form(find_course(course_id))

def course_form(course=None):
    values = {'name': course['name'] if course else ''}
    errors = {}
    if request.method == 'POST':
        values, errors = validate_course(request.form)
        if not errors:
            db = get_db()
            try:
                with db:
                    if course:
                        db.execute('UPDATE courses SET name = ? WHERE id = ?', (values['name'], course['id']))
                    else:
                        db.execute('INSERT INTO courses(name) VALUES (?)', (values['name'],))
            except sqlite3.IntegrityError:
                errors['name'] = 'A course with this name already exists.'
            else:
                flash('Course updated.' if course else 'Course created.')
                return redirect(url_for('courses.index'))
    return render_template('courses/form.html', course=course, values=values, errors=errors), 400 if errors else 200

@bp.post('/<int:course_id>/delete')
def delete(course_id):
    course = find_course(course_id)
    db = get_db()
    try:
        with db:
            db.execute('DELETE FROM courses WHERE id = ?', (course_id,))
    except sqlite3.IntegrityError:
        abort(409, description='This course has assignments. Delete or move those assignments before deleting the course.')
    flash('Course deleted.')
    return redirect(url_for('courses.index'))

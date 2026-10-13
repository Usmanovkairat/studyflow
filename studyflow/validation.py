from datetime import date

PRIORITIES = ('low', 'medium', 'high')
STATUSES = ('todo', 'in_progress', 'done')

def validate_course(form):
    name = form.get('name', '').strip()
    errors = {}
    if not name or len(name) > 100:
        errors['name'] = 'Enter a course name between 1 and 100 characters.'
    return {'name': name}, errors

def validate_task(form, db):
    values = {key: form.get(key, '').strip() for key in ('title', 'course_id', 'due_date', 'notes')}
    values['priority'] = form.get('priority', 'medium')
    values['status'] = form.get('status', 'todo')
    errors = {}
    if not values['title'] or len(values['title']) > 200:
        errors['title'] = 'Enter a title between 1 and 200 characters.'
    if len(values['notes']) > 5000:
        errors['notes'] = 'Notes must be at most 5000 characters.'
    try:
        course_id = int(values['course_id'])
        if not db.execute('SELECT id FROM courses WHERE id = ?', (course_id,)).fetchone():
            raise ValueError
        values['course_id'] = course_id
    except (ValueError, TypeError, OverflowError):
        errors['course_id'] = 'Select an existing course.'
    try:
        if date.fromisoformat(values['due_date']).isoformat() != values['due_date']:
            raise ValueError
    except ValueError:
        errors['due_date'] = 'Enter a real date in YYYY-MM-DD format.'
    for key, allowed in (('priority', PRIORITIES), ('status', STATUSES)):
        if values[key] not in allowed:
            errors[key] = 'Select a valid ' + key + '.'
    return values, errors

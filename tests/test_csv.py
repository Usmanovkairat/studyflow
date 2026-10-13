import csv
import io
import pytest
from studyflow.db import get_db
from studyflow.tasks import csv_safe

@pytest.mark.parametrize('value', ['=1+1','+cmd','-cmd','@SUM(1)','\tcmd','\rcmd','  =cmd',' \tcmd','\n=cmd', '\v=cmd', '\f@cmd', '\u00a0+cmd', '\x00=SUM(1)', '\vplain', '\fplain', '\u00a0\tplain', '  \x7fplain', '\u00a0\x01plain'])
def test_formula_protection(value):
    assert csv_safe(value) == "'" + value

def test_export_parity_quoting_unicode_and_headers(app, client):
    with app.app_context():
        db=get_db()
        db.execute('INSERT INTO courses(name) VALUES(?)', ('=Course',))
        db.executemany('INSERT INTO tasks(title,course_id,due_date,priority,status,notes) VALUES(?,?,?,?,?,?)', [
            ('Математика, "quiz"',1,'2026-10-14','high','todo','First line\nSecond line'),
            ('=formula',1,'2026-10-13','low','done','@notes'),
        ])
        db.commit()
    response=client.get('/tasks/export.csv')
    assert response.status_code == 200
    assert response.mimetype == 'text/csv'
    assert 'attachment;' in response.headers['Content-Disposition']
    rows=list(csv.reader(io.StringIO(response.data.decode('utf-8'))))
    assert rows[0] == ['id','title','course','due_date','priority','status','notes']
    assert [row[0] for row in rows[1:]] == ['2','1']
    assert rows[1][1] == "'=formula" and rows[1][-1] == "'@notes"
    assert rows[2][1] == 'Математика, "quiz"' and rows[2][-1] == 'First line\nSecond line'
    assert rows[2][2] == "'=Course"
    query='q=математика&course_id=1&priority=high&status=todo'
    filtered=list(csv.reader(io.StringIO(client.get('/tasks/export.csv?'+query).data.decode())))
    assert len(filtered) == 2 and filtered[1][0] == '1'
    assert b'1 assignment shown' in client.get('/tasks?'+query).data
    assert b'q=' in client.get('/tasks?'+query).data
    empty=list(csv.reader(io.StringIO(client.get('/tasks/export.csv?q=missing').data.decode())))
    assert empty == [rows[0]]
    for query in ['course_id=99','priority=bad','status=bad']:
        assert client.get('/tasks/export.csv?'+query).status_code == 400


@pytest.mark.parametrize('codepoint', range(0x80, 0xA0))
def test_c1_controls_are_neutralized(codepoint):
    value = chr(codepoint) + 'plain'
    assert csv_safe(value) == "'" + value
    padded = '\u00a0 ' + value
    assert csv_safe(padded) == "'" + padded

import hmac
import os
import secrets
from pathlib import Path
from flask import Flask, abort, render_template, request, session
from .db import close_db, init_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(DATABASE=str(Path(app.instance_path) / 'studyflow.sqlite'),
                            SECRET_KEY=os.environ.get('STUDYFLOW_SECRET_KEY'),
                            SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    if not app.config['SECRET_KEY']:
        if os.environ.get('STUDYFLOW_ENV') == 'production':
            raise RuntimeError('Set STUDYFLOW_SECRET_KEY for production.')
        secret_path = Path(app.instance_path) / 'secret.key'
        try:
            with secret_path.open('x', encoding='utf-8') as file:
                os.chmod(secret_path, 0o600)
                file.write(secrets.token_hex(32))
        except FileExistsError:
            pass
        app.config['SECRET_KEY'] = secret_path.read_text(encoding='utf-8').strip()
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

    def csrf_token():
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_hex(32)
        return session['csrf_token']

    app.jinja_env.globals['csrf_token'] = csrf_token

    @app.before_request
    def protect_mutations():
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            expected = session.get('csrf_token', '')
            supplied = request.form.get('csrf_token', '')
            if not expected or not supplied or not hmac.compare_digest(expected.encode('utf-8'), supplied.encode('utf-8')):
                abort(400, description='Your form expired or has an invalid security token. Reload the page and try again.')

    @app.get('/')
    def dashboard():
        return render_template('dashboard.html')

    @app.errorhandler(400)
    @app.errorhandler(404)
    def error_page(error):
        return render_template('error.html', error=error), error.code

    return app

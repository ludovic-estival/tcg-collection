import functools

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, flash
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return render_template('auth/login.html')
        except db.IntegrityError:
            # Ajouter un message d'erreur sur la page du login
            return redirect(url_for("auth.login"))
        
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect('/')
        
        return render_template('auth/login.html', error=error)
    
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    Execution before the view function.
    This function checks if a user id is stored in the session and gets that user's data from the db.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
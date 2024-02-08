from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('collection', __name__)


def get_collections():
    if g.user != None:
        username = g.user['username']
        collections =  get_db().execute(
            'SELECT * FROM collection WHERE user = ?', [username]
        ).fetchall()

        return collections
    else:
        return None

@bp.route('/')
def index():
    """ 
    Index page.
    """
    collections = get_collections()

    if collections is None:
        return render_template('index.html')
    else:
        return render_template('index.html', collections=collections)
    

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():

    if request.method == 'POST':
        name = request.form['name']
        username = g.user['username']
        db = get_db()
        db.execute('INSERT INTO collection(name, user) VALUES (?, ?)', (name, username))
        db.commit()

    return redirect('/')


@bp.route('/delete/<id>', methods=('GET', 'POST'))
@login_required
def delete(id):
    """
    Delete a collection (and all its content)
    """

    db = get_db()
    db.execute('DELETE FROM contain WHERE idCollection = ?', (id))
    db.execute('DELETE FROM collection WHERE id = ?', (id))
    db.commit()

    return redirect('/')
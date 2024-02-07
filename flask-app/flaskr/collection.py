from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('collection', __name__)


def get_collections():
    username = g.user['username']
    collections =  get_db().execute(
        'SELECT * FROM collection WHERE user = ?', [username]
    ).fetchall()

    return collections

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
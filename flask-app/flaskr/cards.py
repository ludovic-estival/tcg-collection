import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('cards', __name__)

@bp.route('/')
def view_cards():
    db = get_db()
    cards = db.execute('SELECT * FROM card ORDER BY name ASC').fetchall()
    return render_template('index.html', cards=cards, count=len(cards))
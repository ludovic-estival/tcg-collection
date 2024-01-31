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


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        rarity = request.form['rarity']
        price = request.form['price']
        db = get_db()

        if not price:
            db.execute(
                'INSERT INTO card (code, rarity, name)'
                ' VALUES (?, ?, ?)',
                (code, rarity, name)
            )
        else:
            db.execute(
                'INSERT INTO card (code, rarity, name, price)'
                ' VALUES (?, ?, ?, ?)',
                (code, rarity, name, price)
            )
            
        db.commit()
        return redirect('/')

    return render_template('create.html')
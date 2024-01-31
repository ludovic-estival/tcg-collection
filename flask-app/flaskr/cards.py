import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('cards', __name__)

# Get a card from code and rarity
def get_card(code, rarity):
    card = get_db().execute(
        'SELECT * FROM card WHERE code = ? AND rarity = ?',
        (code, rarity)
    ).fetchone()

    if card is None:
        abort(404, f"Card id {code} and rarity {rarity} doesn't exist.")

    return card

# Index page
@bp.route('/')
def view_cards():
    db = get_db()
    cards = db.execute('SELECT * FROM card ORDER BY name ASC').fetchall()
    return render_template('index.html', cards=cards, count=len(cards))


# Add a card form
@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        rarity = request.form['rarity']
        price = request.form['price']
        nbcopy = request.form['nbcopy']
        db = get_db()

        if not price:
            db.execute(
                'INSERT INTO card (code, rarity, name, nbcopy)'
                ' VALUES (?, ?, ?, ?)',
                (code, rarity, name)
            )
        else:
            db.execute(
                'INSERT INTO card (code, rarity, name, price, nbcopy)'
                ' VALUES (?, ?, ?, ?, ?)',
                (code, rarity, name, price)
            )
            
        db.commit()
        return redirect('/')

    return render_template('create.html')

# Update a card
@bp.route('/<code>/<rarity>/update', methods=('GET', 'POST'))
def update(code, rarity):
    card = get_card(code, rarity)

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        nbcopy = request.form['nbcopy']
        db = get_db()

        if not price:
            db.execute(
                'UPDATE card SET name = ?, nbcopy = ?'
                ' WHERE code = ? and rarity = ?',
                (name, code, rarity)
            )
        else:
            db.execute(
                'UPDATE card SET name = ?, price = ?, nbcopy = ?'
                ' WHERE code = ? and rarity = ?',
                (name, price, code, rarity)
            )

        db.commit()
        return redirect('/')

    return render_template('update.html', card=card)

# Delete a card
@bp.route('/<code>/<rarity>/delete', methods=('POST',))
def delete(code, rarity):
    get_card(code, rarity)
    db = get_db()
    db.execute('DELETE FROM card WHERE code = ? and rarity = ?', (code, rarity))
    db.commit()
    return redirect('/')
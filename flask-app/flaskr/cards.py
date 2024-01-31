import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from flaskr.db import get_db

bp = Blueprint('cards', __name__)

# Get a card from code and rarity
# Return card object or None
def get_card(code, rarity):
    card = get_db().execute(
        'SELECT * FROM card WHERE code = ? AND rarity = ?',
        (code, rarity)
    ).fetchone()

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

        if get_card(code, rarity):
            db.execute(
                'UPDATE card SET nbcopy = nbcopy + 1'
                ' WHERE code = ? and rarity = ?',
                (code, rarity))
        else:

            if not price:
                db.execute(
                    'INSERT INTO card (code, rarity, name, nbcopy)'
                    ' VALUES (?, ?, ?, ?)',
                    (code, rarity, name, nbcopy)
                )
            else:
                db.execute(
                    'INSERT INTO card (code, rarity, name, price, nbcopy)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (code, rarity, name, price, nbcopy)
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
                (name, nbcopy, code, rarity)
            )
        else:
            db.execute(
                'UPDATE card SET name = ?, price = ?, nbcopy = ?'
                ' WHERE code = ? and rarity = ?',
                (name, price, nbcopy, code, rarity)
            )

        db.commit()
        return redirect('/')

    return render_template('update.html', card=card)

# Delete a card
@bp.route('/<code>/<rarity>/delete', methods=('POST',))
def delete(code, rarity):
    card = get_card(code, rarity)
    db = get_db()
    delete_card = False

    if card['nbcopy'] > 1:
        db.execute(
            'UPDATE card SET nbcopy = nbcopy - 1'
            ' WHERE code = ? and rarity = ?',
            (code, rarity)
        )
    else:
        db.execute('DELETE FROM card WHERE code = ? and rarity = ?', (code, rarity))
        delete_card = True

    db.commit()

    if not delete_card:
        return redirect(url_for('cards.update', code=card['code'], rarity=card['rarity']))
    else:
        return redirect('/')
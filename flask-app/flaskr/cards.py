import os
import csv
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from werkzeug.utils import secure_filename
from flaskr.db import get_db

bp = Blueprint('cards', __name__)


def get_card(code, rarity):
    """
    Get a card from code and rarity.
    Return a card object or None.
    """
    card = get_db().execute(
        'SELECT card.* FROM card' 
        ' WHERE card.code = ? AND card.rarity = ?',
        (code, rarity)
    ).fetchone()

    return card


def get_rarity():
    """
    Return rarity table content.
    """
    rarities = get_db().execute(
        'SELECT * FROM rarity'
    ).fetchall()

    return rarities


def get_collection_value():
    """
    Return the value of the collection.
    """
    value = get_db().execute(
        'SELECT SUM(price * nbcopy) AS value FROM card'
    ).fetchone()

    return value['value']


@bp.route('/')
def view_cards():
    """ 
    Index page.
    """
    db = get_db()
    cards = db.execute('SELECT card.* from card'
                       ' ORDER BY card.price DESC'
                       ).fetchall()
    value = get_collection_value()
    return render_template('index.html', cards=cards, count=len(cards), value=value)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    """
    Form to add a card.
    """

    codes = get_rarity()
    
    if request.method == 'POST':
        print("coucou2")
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
            db.execute(
                'INSERT INTO card (code, rarity, name, price, nbcopy)'
                ' VALUES (?, ?, ?, ?, ?)',
                (code, rarity, name, price, nbcopy)
            )
            
        db.commit()
        print("ajout BD")
        return redirect(url_for('index'))

    return render_template('create.html', codes=codes)


@bp.route('/<code>/<rarity>/update', methods=('GET', 'POST'))
def update(code, rarity):
    """
    Page of a specific card.
    """
    card = get_card(code, rarity)
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        nbcopy = request.form['nbcopy']
        db = get_db()

        db.execute(
            'UPDATE card SET name = ?, price = ?, nbcopy = ?'
            ' WHERE code = ? and rarity = ?',
            (name, price, nbcopy, code, rarity)
        )

        db.commit()
        return redirect(url_for('index'))

    return render_template('update.html', card=card)


@bp.route('/<code>/<rarity>/delete', methods=('POST', ))
def delete(code, rarity):
    """
    Delete a card.
    """
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


@bp.route('/', methods=('POST', 'GET'))
def insert_from_csv():
    """
    Insert cards from a CSV file.
    """
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        db = get_db()

        with open(f.filename, 'rt', encoding='UTF-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        for card in data:
            card[3] = re.sub(',', '.', card[3])
            card[3] = float(card[3])
            db.execute("INSERT INTO card VALUES (?, ?, ?, ?, ?)", card)

        os.remove(f.filename)
        db.commit()
    return redirect('/')
    
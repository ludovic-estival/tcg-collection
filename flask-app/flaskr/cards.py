import os
import csv
import re

from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('cards', __name__, url_prefix='/collection')


def get_card(id, code, rarity):
    """
    Get a card from code and rarity.
    Return a card object or None.
    """
    card = get_db().execute(
        'SELECT card.*, contain.nbcopy FROM card, contain, collection' 
        ' WHERE contain.idCollection = collection.id AND collection.id = ?'
        ' AND contain.cardcode = card.code AND card.code = ? AND card.rarity = ?',
        (id, code, rarity)
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


def get_cards_number(id):
    """
    Return the number of cards in the collection.
    """
    total = get_db().execute(
        'SELECT SUM(contain.nbcopy) AS value FROM collection, card, contain'
        ' WHERE contain.idCollection = collection.id AND collection.id = ?'
        ' AND contain.cardcode = card.code'
        ' ORDER BY card.code',
        (id)
    ).fetchone()

    return total["value"]


def get_collection_value(id):
    """
    Return the value of the collection.
    """
    value = get_db().execute(
        'SELECT SUM(card.price * contain.nbcopy) AS value FROM collection, card, contain'
        ' WHERE contain.idCollection = collection.id AND collection.id = ?'
        ' AND contain.cardcode = card.code',
        (id)
    ).fetchone()

    return value['value']


def get_collection_content(id):
    """
    Return all the cards of the collection for a specific collection id.
    """
    collection = get_db().execute(
        'SELECT card.code, card.rarity, card.name, card.price, contain.nbcopy'
        ' FROM collection, card, contain'
        ' WHERE contain.idCollection = collection.id AND collection.id = ?'
        ' AND contain.cardcode = card.code'
        ' ORDER BY card.price DESC', 
        (id,)
    ).fetchall()

    return collection


@bp.route('/<id>')
@login_required
def index(id):
    """
    Main page of the collection.
    """

    cards = get_collection_content(id)
    
    if not cards:
        return render_template('collection/index.html', count=0, value=0, id=id)
    else:
        total = get_cards_number(id)
        value = get_collection_value(id)
        return render_template('collection/index.html', cards=cards, count=total, value=round(value, 2), id=id)


@bp.route('/<id>/create', methods=('GET', 'POST'))
@login_required
def create(id):
    """
    Form to add a card.
    """

    codes = get_rarity()
    
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        rarity = request.form['rarity']
        price = request.form['price']
        nbcopy = request.form['nbcopy']
        db = get_db()

        if get_card(id, code, rarity):
            db.execute(
                'UPDATE contain SET nbcopy = nbcopy + ?'
                ' WHERE cardCode = ? AND rarity = ? AND idCollection = ?',
                (nbcopy, code, rarity, id))
        else:
            db.execute(
                'INSERT INTO card (code, rarity, name, price)'
                ' VALUES (?, ?, ?, ?)',
                (code, rarity, name, price)
            )

            db.execute(
                'INSERT INTO contain'
                ' VALUES (?, ?, ?, ?)',
                (id, code, rarity, nbcopy)
            )
            
        db.commit()
        return redirect("/collection/" + str(id))

    return render_template('collection/create.html', codes=codes, id=id)


@bp.route('/<id>/<code>/<rarity>/update', methods=('GET', 'POST'))
@login_required
def update(id, code, rarity):
    """
    Page of a specific card.
    """
    card = get_card(id, code, rarity)
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        nbcopy = request.form['nbcopy']
        db = get_db()

        db.execute(
            'UPDATE card SET name = ?, price = ?'
            ' WHERE code = ? and rarity = ?',
            (name, price, code, rarity)
        )

        db.execute(
            'UPDATE contain SET nbcopy = ?'
            ' WHERE cardCode = ? AND rarity = ? AND idCollection = ?',
            (nbcopy, code, rarity, id)
        )

        db.commit()
        return redirect("/collection/" + str(id))

    return render_template('collection/update.html', card=card, id=id)


@bp.route('/<id>/<code>/<rarity>/delete', methods=('POST', ))
@login_required
def delete(id, code, rarity):
    """
    Delete a card.
    """
    card = get_card(id, code, rarity)
    db = get_db()
    delete_card = False

    if card['nbcopy'] > 1:
        db.execute(
            'UPDATE contain SET nbcopy = nbcopy - 1'
            ' WHERE cardCode = ? AND rarity = ? AND idCollection = ?',
            (code, rarity, id)
        )
    else:
        db.execute('DELETE FROM contain WHERE cardCode = ? AND rarity = ? AND idCollection = ?', (code, rarity, id))
        db.execute('DELETE FROM card WHERE code = ? AND rarity = ?', (code, rarity))
        delete_card = True

    db.commit()

    if not delete_card:
        return redirect("/collection/" + str(id) + "/" + card['code'] + "/" + card['rarity'] + "/update")
    else:
        return redirect("/collection/" + str(id))


@bp.route('/<id>/import', methods=('POST', 'GET'))
@login_required
def insert_from_csv(id):
    """
    Insert cards from a CSV file.
    """
    if request.method == 'POST':
        f = request.files['file']
        
        if re.search('.csv$', f.filename) is None:
            return redirect(url_for('cards.index'))
        
        f.save(f.filename)
        db = get_db()

        with open(f.filename, 'rt', encoding='UTF-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        for card in data:
            if isinstance(card[3], str):
                card[3] = re.sub(',', '.', card[3])
                card[3] = float(card[3])

            copy = card.pop(len(card)-1)

            # code rarity name price --> card 
            # code rarity copy --> contain
            db.execute("INSERT INTO card VALUES (?, ?, ?, ?)", card)
            db.execute("INSERT INTO contain VALUES (?, ?, ?, ?)", (id, card[0], card[1], copy))

        os.remove(f.filename)
        db.commit()
    return redirect("/collection/" + str(id))


@bp.route('/<id>/stats')
@login_required
def stats(id):
    """
    Create and display charts.
    """

    # -- Bar chart: number of cards by rarity

    rarities = get_db().execute('SELECT code FROM rarity').fetchall()
    labelsBar = []
    dataBar = []
    
    for rarity in rarities:
        cards_count = get_db().execute('SELECT SUM(nbcopy) AS number FROM contain'
                                       ' WHERE rarity = ? AND idCollection = ?',
                                        (rarity['code'], id)).fetchone()
        labelsBar.append(rarity["code"])
        dataBar.append(cards_count["number"])

    # -- Line chart: snapshots of the collection (value and number of cards over time)
        
    labelsLine = []
    # Number of cards in the collection
    dataLineNum = [] 
    # Total value of the collection
    dataLineVal = []

    #add_snapshot(id)
    
    snapshots = get_db().execute('SELECT datetime(snapDate) as snapDate, cardsNumber, totalValue FROM snapshot WHERE idCollection = ?', (id,)).fetchall()
    
    for snapshot in snapshots:
        labelsLine.append(snapshot["snapDate"])
        dataLineNum.append(snapshot["cardsNumber"])
        dataLineVal.append(snapshot["totalValue"])
        
    return render_template('collection/stats.html', labelsBar=labelsBar, dataBar=dataBar, labelsLine=labelsLine, dataLineNum=dataLineNum, dataLineVal=dataLineVal, id=id)


# For testing purpose only, will be automated later.
def add_snapshot(id):
    db = get_db()
    db.execute('INSERT INTO snapshot(idCollection, snapDate, cardsNumber, totalValue)'
                     ' VALUES (?, datetime("now"), ?, ?)', (id, get_cards_number(id), get_collection_value(id)))
    db.commit()

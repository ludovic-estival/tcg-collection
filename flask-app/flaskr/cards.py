import functools
import os
import csv

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from werkzeug.utils import secure_filename
from flaskr.db import get_db

bp = Blueprint('cards', __name__)

UPLOAD_FOLDER = '../csv'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return None
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename

# Get a card from code and rarity
# Return card object or None
def get_card(code, rarity):
    card = get_db().execute(
        'SELECT * FROM card WHERE code = ? AND rarity = ?',
        (code, rarity)
    ).fetchone()

    return card

# Get the value of the entire collection
def get_collection_value():
    value = get_db().execute(
        'SELECT SUM(price * nbcopy) AS value FROM card'
    ).fetchone()

    return value['value']

# Index page
@bp.route('/')
def view_cards():
    db = get_db()
    cards = db.execute('SELECT * FROM card ORDER BY name ASC').fetchall()
    value = get_collection_value()
    return render_template('index.html', cards=cards, count=len(cards), value=value)


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
@bp.route('/<code>/<rarity>/delete', methods=('POST', ))
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

@bp.route('/import', methods=('POST', 'GET'))
def insert_from_csv():

    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        db = get_db()

        with open(f.filename, 'rt') as file:
            reader = csv.reader(file)
            data = list(reader)

        for row in data:
            db.execute("INSERT INTO card VALUES (?, ?, ?, ?, ?)", row)

        os.remove(f.filename)
        db.commit()
    return render_template('import.html')
    
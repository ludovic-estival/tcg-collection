import csv
import os
import pytest
import io
from flaskr.db import get_db
from pathlib import Path


def test_index(client, auth):
    auth.login()
    assert client.get('/collection/1').status_code == 200

    auth.login("other", "test")
    assert client.get('/collection/2').status_code == 200


def test_stats(client, auth):
    auth.login()
    assert client.get('/collection/1/stats').status_code == 200


def test_create(client, app, auth):
    auth.login()
    assert client.get('/collection/1/create').status_code == 200
    client.post('/collection/1/create', data={'code': 'MP23-003', 'rarity': 'C', 'name': 'Test-Create', 'price': 10.0, 'nbcopy': 1})

    with app.app_context():
        total = get_db().execute(
            'SELECT SUM(contain.nbcopy) AS value FROM collection, card, contain'
            ' WHERE contain.idCollection = collection.id AND collection.id = 1'
            ' AND contain.cardcode = card.code'
            ' ORDER BY card.code'
        ).fetchone()
        assert total['value'] == 4


def test_create_existing(client, app, auth):
    """
    If an existing card is created, copies number will be increased by one.
    """
    auth.login()
    assert client.get('/collection/1/create').status_code == 200
    client.post('/collection/1/create', data={'code': 'MP23-001', 'rarity': 'PSE', 'name': 'Lovely Labrynth', 'price': 5, 'nbcopy': 2})

    with app.app_context():
        db = get_db()
        card = db.execute("SELECT nbcopy FROM contain"
                          " WHERE cardCode = 'MP23-001' AND rarity = 'PSE'"
                          " AND idCollection = 1").fetchone()
        assert card['nbcopy'] == 4


def test_update(client, app, auth):
    auth.login()
    assert client.get('/collection/1/MP23-001/PSE/update').status_code == 200
    client.post('/collection/1/MP23-001/PSE/update', data={'code': 'MP23-001', 'rarity': 'PSE', 'name': 'Updated', 'price': 10.0, 'nbcopy': 1})

    with app.app_context():
        db = get_db()
        card = db.execute("SELECT card.name FROM card, contain, collection"
                          " WHERE contain.idCollection = collection.id AND collection.id = 1"
                          " AND contain.cardcode = card.code AND card.code = 'MP23-001'"
                          " AND card.rarity = 'PSE'").fetchone()
        assert card['name'] == 'Updated'


def test_card_delete(client, app, auth):
    """
    A card with one copy will be deleted.
    """
    auth.login()
    response = client.post('/collection/1/MP23-002/GR/delete')
    assert response.headers["Location"] == "/collection/1"

    with app.app_context():
        db = get_db()
        card = db.execute("SELECT card.* FROM card, contain, collection"
                          " WHERE contain.idCollection = collection.id AND collection.id = 1"
                          " AND contain.cardcode = card.code AND card.code = 'MP23-002'"
                          " AND card.rarity = 'GR'").fetchone()
        assert card is None
    

def test_copy_delete(client, app, auth):
    """
    If a card has more than one copy, the number of copy will be reduced.
    """
    auth.login()
    response = client.post('/collection/1/MP23-001/PSE/delete')

    assert response.headers["Location"] == "/collection/1/MP23-001/PSE/update"

    with app.app_context():
        db = get_db()
        card = db.execute("SELECT contain.nbcopy FROM card, contain, collection"
                          " WHERE contain.idCollection = collection.id AND collection.id = 1"
                          " AND contain.cardcode = card.code AND card.code = 'MP23-001'"
                          " AND card.rarity = 'PSE'").fetchone()
        assert card["nbcopy"] == 1


def test_csv_import(client, app, auth):
    
    csv_file = Path(__file__).parent / "resources" / "test-csv.csv"

    auth.login()

    response = client.post('/collection/1/import',
                           content_type='multipart/form-data',
                           data={'file': (io.BytesIO(b"Wrong file"), "test.pdf")})
    
    assert response.headers["Location"] == "/collection/1"

    client.post('/collection/1/import', 
                content_type='multipart/form-data', 
                data={'file':( open(csv_file, 'rb'), 'temp-csv.csv')})

    with app.app_context():
        db = get_db()

        card = db.execute("SELECT contain.* FROM contain WHERE cardCode = 'MP23-FR004'"
                          " AND idCollection = 1 AND rarity = 'C'").fetchone()
        assert card is not None

        card = db.execute("SELECT contain.* FROM contain WHERE cardCode = 'MP23-FR005'"
                          " AND idCollection = 1 AND rarity = 'C'").fetchone()
        assert card is not None
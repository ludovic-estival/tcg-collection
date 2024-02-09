import csv
import os
import pytest
from flaskr.db import get_db


def test_index(client, auth):
    auth.login()
    assert client.get('/collection/1').status_code == 200


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


@pytest.mark.skip(reason="Test not working, to complete later.")
def test_csv_import(client, app):
    rows = [ 
            ['MP23-FR004', 'C', 'TestCSV', '4', '1'],
            ['MP23-FR005', 'C', 'TestCSV', '4', '1']
            ]
    
    file = 'temp-csv.csv'
    
    with open('temp-csv.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(rows)

    data = {
        'field': 'file',
        'file': (open(file, 'rb'), file)
    }

    client.post('/import', data=data, buffered=True, content_type="multipart/form-data")

    with app.app_context():
        db = get_db()

        card = db.execute("SELECT * FROM card WHERE code = 'MP23-FR004'").fetchone()
        assert card is not None

        card = db.execute("SELECT * FROM card WHERE code = 'MP23-FR005'").fetchone()
        assert card is not None

    os.remove('temp-csv.csv')


import csv
import os
import pytest
from flaskr.db import get_db


def test_index(client):
    assert client.get('/').status_code == 200
    

def test_create(client, app, auth):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'code': 'MP23-003', 'rarity': 'C', 'name': 'Test-Create', 'price': 10.0, 'nbcopy': 1})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(code) FROM card').fetchone()[0]
        assert count == 3


def test_create_existing(client, app, auth):
    """
    If an existing card is created, copies number will be increased by one.
    """
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'code': 'MP23-001', 'rarity': 'PSE', 'name': 'Lovely Labrynth', 'price': 5, 'nbcopy': 2})

    with app.app_context():
        db = get_db()
        card = db.execute("SELECT * FROM card WHERE code = 'MP23-001'").fetchone()
        assert card['nbcopy'] == 3


def test_update(client, app, auth):
    auth.login()
    assert client.get('/MP23-001/PSE/update').status_code == 200
    client.post('/MP23-001/PSE/update', data={'code': 'MP23-001', 'rarity': 'PSE', 'name': 'Updated', 'price': 10.0, 'nbcopy': 1})

    with app.app_context():
        db = get_db()
        card = db.execute("SELECT * FROM card WHERE code = 'MP23-001'").fetchone()
        assert card['name'] == 'Updated'


def test_card_delete(client, app, auth):
    """
    A card with one copy will be deleted.
    """
    auth.login()
    response = client.post('/MP23-002/GR/delete')
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        card = db.execute("SELECT * FROM card WHERE code = 'MP23-002'").fetchone()
        assert card is None
    

def test_copy_delete(client, app, auth):
    """
    If a card has more than one copy, the number of copy will be reduced.
    """
    auth.login()
    response = client.post('/MP23-001/PSE/delete')

    assert response.headers["Location"] == "/MP23-001/PSE/update"

    with app.app_context():
        db = get_db()
        card = db.execute("SELECT * FROM card WHERE code = 'MP23-001'").fetchone()
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


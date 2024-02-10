import pytest
from flaskr.db import get_db


def test_index(client, auth):
    # No user connection
    assert client.get('/').status_code == 200

    # User with no collections
    auth.login('other', 'test')
    assert client.get('/').status_code == 200

    # User with collections
    auth.login('test', 'test')
    assert client.get('/').status_code == 200
    
    
def test_create(client, app, auth):
    auth.login()
    response = client.post('/create', data={'name': 'collection3', 'username': 'test'})
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        collection = db.execute("SELECT * FROM collection" 
                                " WHERE user = 'test' AND name = 'collection3'").fetchone()
        assert collection is not None


def test_delete(client, app, auth):
    auth.login()
    response = client.post('/delete/3')
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        collection = db.execute("SELECT * FROM collection" 
                                " WHERE user = 'test' AND name = 'collection3'").fetchone()
        assert collection is None
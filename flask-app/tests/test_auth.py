import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    client.post('/auth/register', data={'username': 'a', 'password': 'a'})
    
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


def test_already_registered(client):
    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register', data={'username': 'test', 'password': 'test'})
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_wrong_username_and_pwd(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

    
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


def test_login_required(client):
    response = client.get('/create')
    assert response.headers["Location"] == "/auth/login"
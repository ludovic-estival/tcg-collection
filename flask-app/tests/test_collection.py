import pytest
from flaskr.db import get_db


def test_create(client, app, auth):
    auth.login()
    assert client.get('/').status_code == 200
    return 0
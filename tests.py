import time

import pytest

from init import create_app
from lib import create_fibonacci


@pytest.fixture(scope="session")
def app():
    app = create_app(__name__)
    return app


@pytest.fixture(autouse=True)
def db(app):
    from extensions.sqlalchemy import db
    # setup
    with app.app_context():
        db.create_all()
    yield
    # teardown
    with app.app_context():
        db.drop_all()


def test_create_fibonacci():
    fibonacci_series = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5),
                        (6, 8), (7, 13)]
    for o, nth in fibonacci_series:
        fibo = create_fibonacci(o)
        assert type(fibo) == int
        assert fibo == nth


def test_create_fibonacci_route(app):
    with app.test_client() as client:
        test_value = 10
        test_result = create_fibonacci(test_value)
        response = client.post('/fibonacci/', json={"n": test_value})
        assert response.status_code == 202
        assert response.json == {"status": "pending"}

        time.sleep(5)
        response = client.post('/fibonacci/', json={"n": test_value})
        assert response.status_code == 200
        assert response.json == {"status": "success", "nth": str(test_result)}

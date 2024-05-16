"""
test cache/main.py
"""

from fastapi.testclient import TestClient

from main import app
from user import MAXUSERS

client = TestClient(app)


def test_read_root():
    """reports no hit at init"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"nhit": 0}


def test_user_read_single():
    """can reply to a valid user request"""
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "User1"}


def test_user_read_fail_invalid_user():
    """fails gracefully to an invalid user request"""

    tests = {
        "/user/0": "invalid uid: 0",
        f"/user/{MAXUSERS + 1}": f"invalid uid: {MAXUSERS + 1}",
    }

    for path, expected in tests.items():
        response = client.get(path)
        assert response.status_code == 404
        assert response.json() == {"detail": expected}


def test_user_read_all():
    """replies to all valid requests"""

    requests = [f"/user/{i}" for i in range(1, MAXUSERS + 1)]
    responses = [{"id": i, "name": f"User{i}"} for i in range(1, MAXUSERS + 1)]

    for req, rep in zip(requests, responses):
        response = client.get(req)
        assert response.status_code == 200
        assert response.json() == rep


def test_user_read_cache_db_replies():
    """replies to all valid requests"""

    # read all two times
    for req in [f"/user/{i}" for i in range(1, MAXUSERS + 1)]:
        client.get(req)

    for req in [f"/user/{i}" for i in range(1, MAXUSERS + 1)]:
        client.get(req)

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"nhit": MAXUSERS}
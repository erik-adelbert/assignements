"""
test cache/main.py
"""

from fastapi.testclient import TestClient

from app.main import app
from app.user import MAXUSERS

XTOKEN = "shush"

client = TestClient(app)


def test_root_read_fail_with_bad_token():
    """returns 400 error with bad token"""
    response = client.get("/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_root_read():
    """reports no hit at init"""
    response = client.get("/", headers={"X-Token": XTOKEN})
    assert response.status_code == 200
    assert response.json() == {"nhit": 0}


def test_user_read_fail_with_bad_token():
    """returns 400 error with bad token"""
    response = client.get("/user/1", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_user_read_single():
    """can reply to a valid user request"""
    response = client.get("/user/1", headers={"X-Token": XTOKEN})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "User1"}


def test_user_read_fail_invalid_user():
    """fails gracefully to an invalid user request"""

    tests = {
        "/user/0": "Invalid uid: 0",
        f"/user/{MAXUSERS + 1}": f"Invalid uid: {MAXUSERS + 1}",
    }

    for path, expected in tests.items():
        response = client.get(path, headers={"X-Token": XTOKEN})
        assert response.status_code == 404
        assert response.json() == {"detail": expected}


def test_user_read_all():
    """replies to all valid requests"""

    requests = [f"/user/{i}" for i in range(1, MAXUSERS + 1)]
    responses = [{"id": i, "name": f"User{i}"} for i in range(1, MAXUSERS + 1)]

    for req, rep in zip(requests, responses):
        response = client.get(req, headers={"X-Token": XTOKEN})
        assert response.status_code == 200
        assert response.json() == rep


def test_user_read_cache_db_replies():
    """replies to all valid requests"""

    # read all users twice
    for _ in range(2):
        for req in [f"/user/{i}" for i in range(1, MAXUSERS + 1)]:
            _ = client.get(req, headers={"X-Token": XTOKEN})  # discard response

    # assert that cache have halved the hits on db
    response = client.get("/", headers={"X-Token": XTOKEN})
    assert response.status_code == 200
    assert response.json() == {"nhit": MAXUSERS}

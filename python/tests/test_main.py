"""
test_main.py --
Unit tests

erik@adelbert.fr - 2024/05
"""

from asyncio import gather
from pytest import mark

# from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.user import MAXUSERS

XTOKEN = "shush"

client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@mark.asyncio
async def test_root_read_fail_with_bad_token():
    """Returns 400 error with bad token"""
    response = await client.get("/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


@mark.asyncio
async def test_root_read():
    """Reports no hit at init"""
    # this test as its own context
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/", headers={"X-Token": XTOKEN})
    assert response.status_code == 200
    assert response.json() == {"nhit": 0}


@mark.asyncio
async def test_user_read_fail_with_bad_token():
    """Returns 400 error with bad token"""
    response = await client.get("/user/1", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


@mark.asyncio
async def test_user_read_single():
    """Replies to a valid user request"""
    response = await client.get("/user/1", headers={"X-Token": XTOKEN})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "User1"}


@mark.asyncio
async def test_user_read_fail_invalid_user():
    """Fails gracefully to an invalid user request"""
    tests = {
        "/user/0": "Invalid uid: 0",
        f"/user/{MAXUSERS + 1}": f"Invalid uid: {MAXUSERS + 1}",
    }

    responses = await gather(
        *((client.get(url, headers={"X-Token": XTOKEN}) for url in tests))
    )
    return all(a.json() == b for a, b in zip(responses, tests.values()))


@mark.asyncio
async def test_user_read_all():
    """Replies to all valid requests"""

    requests = [f"/user/{i}" for i in range(1, MAXUSERS + 1)]
    expected = ({"id": i, "name": f"User{i}"} for i in range(1, MAXUSERS + 1))

    responses = await gather(
        *((client.get(url, headers={"X-Token": XTOKEN}) for url in requests))
    )
    return (r.json() for r in responses) == expected


@mark.asyncio
async def test_user_read_cache_db_replies():
    """Replies to all valid requests"""

    requests = [f"/user/{i}" for i in range(1, MAXUSERS + 1)]

    # read all users twice
    for _ in range(2):
        _ = await gather(
            *((client.get(url, headers={"X-Token": XTOKEN}) for url in requests))
        )

    # assert that cache have halved the hits on db
    response = await client.get("/", headers={"X-Token": XTOKEN})
    assert response.status_code == 200
    assert response.json() == {"nhit": MAXUSERS}

"""
test_main.py --
Unit tests

erik@adelbert.fr - 2024/05
"""

from asyncio import gather
from collections import namedtuple
from pytest import mark

from httpx import AsyncClient, ASGITransport

from app.main import app
from app.user import MAXUSERS


def new_client():
    """Create a new asynchronous HTTP client for testing."""
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


# Global async client and token
CLIENT = new_client()
XTOKEN = "shush"


async def fetch(path, ac=CLIENT, token=XTOKEN):
    """Helper function to fetch a single URL"""
    return await ac.get(path, headers={"X-Token": token})


async def fetch_many(urls, ac=CLIENT, token=XTOKEN):
    """Helper function to fetch multiple URLs concurrently"""
    return await gather(*((fetch(url, ac, token) for url in urls)))


# Generic unit test factories
def create_single(coro, code, expected):
    """
    Returns an async unit test for a single request.

    :param coro: The coroutine to execute.
    :param code: The expected status code.
    :param expected: The expected JSON response.
    """

    @mark.asyncio
    async def _unit():
        # Replace this with your actual async test logic
        response = await coro
        assert response.status_code == code
        assert response.json() == expected

    return _unit


def create_batch(requests, expected):
    """
    Returns an async unit test for multiple requests.

    :param requests: The list of URLs to fetch.
    :param expected: The expected JSON responses.
    """

    @mark.asyncio
    async def _unit():
        responses = await fetch_many(requests)
        assert tuple(r.json() for r in responses) == tuple(expected)

    return _unit


# Define namedtuples for test cases
UnaryTest = namedtuple("UnaryTest", "coro code expected")
BatchTest = namedtuple("BatchTest", "requests expected")

# Single request based tests
singles = {
    "root_read_fail_with_bad_token": UnaryTest(
        coro=fetch("/", token="coneofsilence"),
        code=400,
        expected={"detail": "Invalid X-Token header"},
    ),
    "root_read": UnaryTest(
        coro=fetch("/", new_client()),  # this test has its own context
        code=200,
        expected={"nhit": 0},
    ),
    "user_read_fail_with_bad_token": UnaryTest(
        coro=fetch("/user/1", token="coneofsilence"),
        code=400,
        expected={"detail": "Invalid X-Token header"},
    ),
    "user_read_fail_with_badly_typed_request": UnaryTest(
        coro=fetch("/user/morty"),
        code=422,
        expected={
            "detail": [
                {
                    "input": "morty",
                    "loc": ["path", "user_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "type": "int_parsing",
                }
            ]
        },
    ),
    "user_read_single": UnaryTest(
        coro=fetch("/user/1"),
        code=200,
        expected={"id": 1, "name": "User1"},
    ),
}


def _bad_id(uid):
    return {"detail": f"Invalid uid: {uid}"}


def _all_users():
    return (f"/user/{i}" for i in range(1, MAXUSERS + 1))


# Multiple requests based tests
batches = {
    "user_read_fail_invalid_user": BatchTest(
        requests=(f"/user/{id}" for id in (-1, 0, MAXUSERS + 1)),
        expected=(_bad_id(id) for id in (-1, 0, MAXUSERS + 1)),
    ),
    "user_read_all": BatchTest(
        requests=_all_users(),
        expected=({"id": i, "name": f"User{i}"} for i in range(1, MAXUSERS + 1)),
    ),
}


# Dynamically create test functions and add them to the global namespace
# Test function names are appended "test_" prefix: ex. "user_read_all" -> test_user_readall()
for tests, factory in ((singles, create_single), (batches, create_batch)):
    for name, test in tests.items():
        globals()[f"test_{name}"] = factory(*test)


# Non-generic tests
@mark.asyncio
async def test_user_read_cache_db_replies():
    """Replies to all requests by hitting cache first"""

    requests = _all_users()

    # read all users twice
    _ = await fetch_many(tuple(requests) * 2)

    # ensure cache have halved the hits on db
    await create_single(
        coro=fetch("/"),
        code=200,
        expected={"nhit": MAXUSERS},
    )()

"""
test_user.py --
Unit tests

erik@adelbert.fr - 2024/05
"""

from dataclasses import asdict
from pydantic_core import ValidationError
from pytest import mark, raises

from app.user import User, UserService, MAXUSERS


def test_new_user():
    """Instantiates an empty User"""
    user = User()
    assert user.id == 0 and user.name == ""


def test_new_user_with_valid_args():
    """Instantiates a User from args"""
    user = User(id=1, name="Rick")
    assert user.id == 1 and user.name == "Rick"


def test_new_user_validates_args_or_fails():
    """Raises a pydantic ValidationError"""
    with raises(ValidationError):
        _ = User(id="Morty", name=1)


def test_new_user_service():
    """Instantiates a user service"""
    user_service = UserService()
    assert user_service.nhit == 0
    assert len(user_service.db) == MAXUSERS
    assert asdict(user_service.db[1]) == {"id": 1, "name": "User1"}
    assert asdict(user_service.db[MAXUSERS]) == {
        "id": MAXUSERS,
        "name": f"User{MAXUSERS}",
    }


USER_SERVICE = UserService()


@mark.asyncio
async def test_user_service_initial_hit_count_is_zero():
    """Returns initial nhit=0"""
    nhit = await USER_SERVICE.hits()
    assert nhit == 0


@mark.asyncio
async def test_user_service_expected_user():
    """Returns the expected user"""

    user = await USER_SERVICE.user(MAXUSERS)
    assert user == User(id=MAXUSERS, name=f"User{MAXUSERS}")


@mark.asyncio
async def test_user_service_raise_valuerror():
    """Raises Valuerror on bad user id"""

    with raises(ValueError):
        await USER_SERVICE.user(MAXUSERS + 1)

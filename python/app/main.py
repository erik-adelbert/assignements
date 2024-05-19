"""
main.py --
This is a toy FastAPI app.

It defines a FastAPI application that provides user information 
services. It features a single dataclass-based user info service, 
mocks database accesses with an in-memory cache, and works 
asynchronously. The endpoints use Pydantic for validation and 
implement  a simple token-based authorization.

erik@adelbert.fr - 2024/05
"""

from dataclasses import asdict
from typing import Annotated
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from app.user import UserService


user_service = UserService()
app = FastAPI()


class HitModel(BaseModel):
    """Hit validation model"""

    nhit: int


@app.get("/", response_model=HitModel)
async def read_root(x_token: Annotated[str, Header()]):
    """Return the current number od db hits"""
    check_token(x_token)

    return HitModel(nhit=await user_service.hits())


class UserModel(BaseModel):
    """User validation model"""

    id: int
    name: str


@app.get("/user/{user_id}", response_model=UserModel)
async def read_user(user_id: int, x_token: Annotated[str, Header()]):
    """Return the given user info"""
    check_token(x_token)

    try:
        response = asdict(await user_service.user(user_id))
        return UserModel.model_validate(response)
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err


FAKETOKEN = "shush"


def check_token(x_token: str) -> None | Exception:
    """Check x_token against the fake token"""
    if x_token != FAKETOKEN:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

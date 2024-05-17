"""
Async cached db access toy main file
"""

from typing import Annotated
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from user import UserService

FAKETOKEN = "shush"

user_service = UserService()
app = FastAPI()


class HitModel(BaseModel):
    """hit model"""

    nhit: int


@app.get("/", response_model=HitModel)
async def read_root(x_token: Annotated[str, Header()]):
    """
    Returns the current number od db hits
    """
    if x_token != FAKETOKEN:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    return await user_service.hits()


class UserModel(BaseModel):
    """user model"""

    id: int
    name: str


@app.get("/user/{user_id}", response_model=UserModel)
async def read_user(user_id: int, x_token: Annotated[str, Header()]):
    """
    Returns the given user info
    """

    if x_token != FAKETOKEN:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    try:
        response = await user_service.user(user_id)
        return response
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err

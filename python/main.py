"""
Async cached db access toy main file
"""

from fastapi import FastAPI, HTTPException
from user import UserService

user_service = UserService()

app = FastAPI()


@app.get("/")
async def read_root():
    """
    Returns the current number od db hits
    """
    return await user_service.hits()


@app.get("/user/{user_id}")
async def read_user(user_id: int):
    """
    Returns the given user info
    """

    try:
        response = await user_service.user(user_id)
        return response
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err

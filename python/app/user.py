"""
user.py --
UserService class uses an in-memory cache to store and retrieve
user data, reducing the load on the simulated database. It employs 
asynchronous methods to simulate database access and uses caching to 
optimize performance:

 - The User class models user information with simple fields.
 - The UserService class handles the logic for caching, retrieving 
   user data, and tracking database hits.

erik@adelbert.fr - 2024/05
"""

from asyncio import sleep
from typing import Dict
from dataclasses import field
from pydantic.dataclasses import dataclass

from app.cache import async_lru_cache

MAXUSERS = 1000
DBRTT = 3e-3  # 3ms


@dataclass(slots=True)
class User:
    """User infos"""

    id: int = 0
    name: str = ""


@dataclass(slots=True)
class UserService:
    """User info service from a cached DB"""

    db: Dict[int, User] = field(init=False, default=False)
    nhit: int = field(init=False, default=0)

    def __hash__(self):
        return hash(str(self.db))

    def __post_init__(self):
        self.db = {i: User(id=i, name=f"User{i}") for i in range(1, MAXUSERS + 1)}

    @async_lru_cache(maxsize=MAXUSERS)
    async def user(self, uid: int) -> User:
        """Return user infos"""
        if uid < 1 or uid > MAXUSERS:
            raise ValueError(f"Invalid uid: {uid}")

        self.nhit += 1
        await sleep(DBRTT)  # db round-trip

        return self.db[uid]

    async def hits(self) -> int:
        """Return the current count of db hits"""
        return self.nhit

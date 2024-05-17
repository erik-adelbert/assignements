"""
DBAccess caching toy example
"""

from asyncio import sleep
from typing import Dict
from dataclasses import field
from pydantic.dataclasses import dataclass

from cache import async_lru_cache

MAXUSERS = 100
DBRTT = 3e-3  # 3ms


@dataclass(slots=True)
class User:
    """
    User infos
    """

    id: int = 0
    name: str = ""


@dataclass(slots=True)
class UserService:
    """
    Serve user info from a cached DB
    """

    db: Dict[int, User] = field(init=False, default=False)
    nhit: int = field(init=False, default=0)

    def __hash__(self):
        return hash(str(self.db))

    def __post_init__(self):
        self.db = {i: User(id=i, name=f"User{i}") for i in range(1, MAXUSERS + 1)}

    async def _async_init(self):
        await sleep(DBRTT)  # db round-trip
        return self

    @async_lru_cache(maxsize=MAXUSERS)
    async def user(self, uid: int) -> User:
        """
        Serve user infos from
        """
        if uid < 1 or uid > MAXUSERS:
            raise ValueError(f"Invalid uid: {uid}")

        self.nhit += 1
        await sleep(DBRTT)  # db round-trip

        return self.db[uid]

    async def hits(self) -> int:
        """
        Serve the current number of db hits
        """
        return self.nhit

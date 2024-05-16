"""
DBAccess caching toy example
"""

from asyncio import sleep
from dataclasses import asdict, dataclass, field
from typing import Dict

from cache import async_lru_cache

MAXUSERS = 100
SLEEP_DURATION = 3e-3  # 3 ms sleep
# SLEEP_DURATION = 3e-6  # 3 μs sleep


@dataclass
class User:
    """
    User infos
    """

    id: int = 0
    name: str = ""


@dataclass
class UserService:
    """
    Serve user info from a cached DB
    """

    db: Dict[int, User] = field(init=False, default=False)
    nhit: int = field(init=False, default=0)

    def __await__(self):
        self._async_init().__await__()

    def __hash__(self):
        return hash(repr(self.db))

    def __eq__(self, other):
        return repr(self.db) == repr(other)

    def __post_init__(self):
        self.db = {i: User(id=i, name=f"User{i}") for i in range(1, MAXUSERS + 1)}

    async def _async_init(self):
        await sleep(SLEEP_DURATION)  # db round-trip
        return self

    @async_lru_cache(maxsize=MAXUSERS)
    async def user(self, uid: int) -> Dict[str, any]:
        """
        Serve user infos from
        """
        if uid < 1 or uid > MAXUSERS:
            raise ValueError(f"invalid uid: {uid}")

        self.nhit += 1
        await sleep(SLEEP_DURATION)  # db round-trip

        return asdict(self.db[uid])

    async def hits(self) -> Dict[str, int]:
        """
        Serve the current number of db hits
        """
        return {"nhit": self.nhit}

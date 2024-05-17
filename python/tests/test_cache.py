"""
test cache/cache.py
"""

from pytest import mark
from app.cache import async_lru_cache


@mark.asyncio
async def test_async_cache_decorator_should_cache_async_func():
    """
    Interposes cache when called
    """
    pid = _positive()

    @async_lru_cache(maxsize=2)
    async def to_be_decorated(key: int) -> int:
        _ = key
        return next(pid)

    assert await to_be_decorated(0xDEADBEEF) == 1
    assert await to_be_decorated(0x8BADF00D) == 2
    assert await to_be_decorated(0xDEADBEEF) == 1  # next is not called again


def _positive():
    i = 1
    while True:
        yield i
        i += 1

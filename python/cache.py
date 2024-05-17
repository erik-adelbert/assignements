"""
cache.py -- 
pythonic async in-memory cache
"""

from asyncio import ensure_future
from functools import lru_cache


def async_lru_cache(*args, **kwargs):
    """decorator with options"""

    def async_lru_cache_decorator(
        async_function,
    ):
        @lru_cache(*args, **kwargs)
        def cached_async_function(*args, **kwargs):
            coroutine = async_function(*args, **kwargs)
            return ensure_future(coroutine)

        return cached_async_function

    return async_lru_cache_decorator

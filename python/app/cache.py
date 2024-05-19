"""
cache.py -- 
A pythonic async in-memory cache

It provides a way to cache the results of asynchronous functions using 
the lru_cache mechanism. It uses ensure_future to ensure the coroutine 
is scheduled and a Future object is returned, making it compatible with 
asynchronous code. The async_lru_cache decorator is flexible and allows 
passing arguments to customize the behavior of the underlying lru_cache.

erik@adelbert.fr - 2024/05
"""

from asyncio import ensure_future
from functools import lru_cache


def async_lru_cache(*lru_cache_args, **lru_cache_kwargs):
    """Decorator with lru_cache options"""

    def async_lru_cache_decorator(
        async_function,
    ):

        @lru_cache(*lru_cache_args, **lru_cache_kwargs)
        def cached_async_function(*fun_args, **fun_kwargs):
            coroutine = async_function(*fun_args, **fun_kwargs)
            return ensure_future(coroutine)

        return cached_async_function

    return async_lru_cache_decorator

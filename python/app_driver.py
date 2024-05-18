"""
UserService API driver
"""

import asyncio
import time
import sys
import aiohttp

FASTAPI = "http://127.0.0.1"
APIPORT = 8000
XTOKEN = "shush"
MAXUSERS = 1000
FACTOR = 10

try:
    port = int(sys.argv[1])
except (ValueError, IndexError):
    port = APIPORT  # pylint: disable=invalid-name

requests = [f"{FASTAPI}:{port}/user/{i}" for i in range(1, MAXUSERS + 1)]


async def get(url, session):
    """
    request one
    """
    try:
        async with session.get(url=url, headers={"X-Token": XTOKEN}) as response:
            await response.read()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Unable to get url {url} due to { e.__class__}.")


async def main(urls):
    """
    driver
    """
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*(get(url, session) for url in urls))
    print(f"Finalized all. Return is a list of len {len(ret)} outputs.")


start = time.time()
asyncio.run(main(requests * FACTOR))
end = time.time()

top = int((end - start) * 1_000_000 / (MAXUSERS * FACTOR))  # time per op in μs

print(
    f"Took {end - start:.2f} seconds to pull {MAXUSERS * FACTOR} requests: {top}μs/op"
)

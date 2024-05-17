"""
UserService API driver
"""

import asyncio
import time
import aiohttp

FASTAPI = "http://127.0.0.1:8000"
XTOKEN = "shush"
MAXUSERS = 100
FACTOR = 100

requests = [f"{FASTAPI}/user/{i}" for i in range(1, MAXUSERS + 1)]


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

print(f"Took {end - start} seconds to pull {len(requests) * FACTOR} requests.")

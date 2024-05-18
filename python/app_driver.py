"""
app_driver.py --
UserService API basic driver

erik@adelbert.fr - 2024/05
"""

import asyncio
import time
import random
import sys
import aiohttp

FASTAPI = "http://127.0.0.1"
APIPORT = 8000
XTOKEN = "shush"
MAXUSERS = 1000
FACTOR = 10

# get api port
try:
    port = int(sys.argv[1])
except (ValueError, IndexError):
    port = APIPORT  # pylint: disable=invalid-name


# build requests
requests = [
    f"{FASTAPI}:{port}/user/{i}" for i in range(1, MAXUSERS + int(MAXUSERS / 4))
]  # MAXUSERS good id + 25% bad id requests

random.shuffle(requests)  # fischer-yeats
requests = requests[:MAXUSERS]  # still 4/1 good vs. bad ratio


async def get(url, session):
    """Request one"""
    try:
        async with session.get(url=url, headers={"X-Token": XTOKEN}) as response:
            return await response.read()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Unable to get url {url} due to { e.__class__}.")


async def main(urls):
    """Request all"""
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(get(url, session) for url in urls))


# run requests
start = time.time()
responses = asyncio.run(main(requests * FACTOR))
end = time.time()

# acknowledge termination
nresponses = len(responses)
out = [f"Finalized all. Return is a list of len {nresponses} outputs."]

# build stats
if nresponses:
    nerrors: int = len(
        list(
            filter(
                lambda x: x if x and "Invalid" in x.decode("ascii") else False,
                responses,
            )
        )
    )
    nsuccess: int = len(
        list(
            filter(
                lambda x: x if x and "name" in x.decode("ascii") else False,
                responses,
            )
        )
    )

    def _percent(x: int) -> int:
        return round(x / nresponses * 100)

    ok, nok = _percent(nsuccess), _percent(nerrors)
    nhard = _percent(nresponses - (nsuccess + nerrors))  # expect 0

    out.append(
        f"\nResponses ratios | 200: {ok}% | 404: {nok}% | hard errors: {nhard}% | "
        "(expected: ~ 80/20/0)"
    )

# compute time per op
μs = 1_000_000  # pylint: disable=non-ascii-name, invalid-name
δt, N = end - start, MAXUSERS * FACTOR  # pylint: disable=non-ascii-name, invalid-name
out.append(f"\nTook ~{δt:.2f} seconds to pull {N} requests: {int(δt / N * μs)}μs/op")

# display results
print("\n".join(out))

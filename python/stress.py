"""
stress.py --

This script performs a stress test on the UserService API by sending multiple
concurrent requests, measures the time taken for the operations, and analyzes
the responses to determine the success and error rates. The final output 
provides a summary of the performance and response statistics.

```bash
❯ make stress-test
python stress.py 8000
Running 10000 concurrent requests against http://127.0.0.1:8000/user
Finalized all. Return is a list of len 10000 outputs.

Responses ratio | 200: 80% | 404: 20% | unexpected: 0% | (expected: ~ 80/20/0)

Took ~5.51 seconds to pull 10000 requests: 551μs/op
```

erik@adelbert.fr
"""

from asyncio import gather, run
from datetime import datetime, timedelta
from random import shuffle

import sys

from aiohttp import ClientSession


# Constants and Initialization
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


# Building and Shuffling Requests
requests = [
    f"{FASTAPI}:{port}/user/{i}" for i in range(1, MAXUSERS + int(MAXUSERS / 4))
]  # MAXUSERS good id + 25% bad id requests

shuffle(requests)  # fischer-yeats
requests = requests[:MAXUSERS]  # still 4/1 good vs. bad ratio


# Asynchronous Request Function
async def get(url, session):
    """Request one"""
    try:
        async with session.get(url=url, headers={"X-Token": XTOKEN}) as response:
            return await response.read()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Unable to get url {url} due to { e.__class__}.")


# Main Asynchronous Function
async def main(urls):
    """Request all"""
    async with ClientSession() as session:
        return await gather(*(get(url, session) for url in urls))


# Execution and Timing
N = MAXUSERS * FACTOR

print(f"Running {N} concurrent requests against {FASTAPI}:{APIPORT}/user")
dt = datetime.now()
responses = run(main(requests * FACTOR))
dt = datetime.now() - dt

# Response Analysis
nresponse = len(responses)
out = [f"Finalized all. Return is a list of len {nresponse} outputs."]

# Basic stats
if nresponse:

    def _percent(x: int) -> int:
        return round(x / nresponse * 100)

    def _count(pattern: str):
        return sum(1 for r in responses if r and pattern in r.decode("ascii"))

    nerror, nsuccess = map(_count, ("Invalid", "name"))
    unknown = nresponse - (nsuccess + nerror)

    ok, nok, unxp = map(_percent, (nsuccess, nerror, unknown))
    out.append(
        f"Responses ratio | 200: {ok}% | 404: {nok}% | unexpected: {unxp}% | "
        "(expected: ~ 80/20/0)"
    )

# Timing and Final Output
s = timedelta(seconds=1)
μs = timedelta(microseconds=1)  # pylint: disable=non-ascii-name, invalid-name
out.append(f"Took ~{dt/s:.2f} seconds to pull {N} requests: {(dt/N)/μs:.0f}μs/op")

print("\n\n".join(out))

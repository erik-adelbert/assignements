"""
stress.py --

This script performs a stress test on the UserService API by sending multiple
concurrent requests, measures the time taken for the operations, and analyzes
the responses to determine the success and error rates. The final output 
provides a summary of the performance and response statistics.

```bash
❯ make stress-test
python stress.py 8000
Finalized all. Return is a list of len 10000 outputs.

Responses ratios | 200: 80% | 404: 20% | hard errors: 0% | (expected: ~ 80/20/0)

Took ~5.45 seconds to pull 10000 requests: 544μs/op
```

erik@adelbert.fr
"""

import asyncio
import time
import random
import sys
import aiohttp

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

random.shuffle(requests)  # fischer-yeats
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
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(get(url, session) for url in urls))


# Execution and Timing
start = time.time()
responses = asyncio.run(main(requests * FACTOR))
end = time.time()

# Response Analysis
nresponses = len(responses)
out = [f"Finalized all. Return is a list of len {nresponses} outputs."]

# Basic stats
if nresponses:
    nerrors = sum(1 for r in responses if r and "Invalid" in r.decode("ascii"))
    nsuccess = sum(1 for r in responses if r and "name" in r.decode("ascii"))

    def _percent(x: int) -> int:
        return round(x / nresponses * 100)

    ok, nok = _percent(nsuccess), _percent(nerrors)
    nhard = _percent(nresponses - (nsuccess + nerrors))  # expect 0

    out.append(
        f"\nResponses ratios | 200: {ok}% | 404: {nok}% | hard errors: {nhard}% | "
        "(expected: ~ 80/20/0)"
    )

# Timing and Final Output
μs = 1_000_000  # pylint: disable=non-ascii-name, invalid-name
δt, N = end - start, MAXUSERS * FACTOR  # pylint: disable=non-ascii-name, invalid-name
out.append(f"\nTook ~{δt:.2f} seconds to pull {N} requests: {int(δt / N * μs)}μs/op")

print("\n".join(out))

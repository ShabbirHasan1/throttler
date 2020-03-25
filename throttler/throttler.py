import asyncio
import time
from collections import deque


class Throttler:
    """
    Context manager for limiting rate of accessing to context block.

    Example usages:
        - https://github.com/uburuntu/throttler/blob/master/examples/example_throttlers.py
        - https://github.com/uburuntu/throttler/blob/master/examples/example_throttlers_aiohttp.py
    """
    __slots__ = ('_rate_limit', '_period', '_times',)

    def __init__(self, rate_limit: int, period: float = 1.0):
        self._rate_limit = rate_limit
        self._period = period

        self._times = deque()

    async def __aenter__(self):
        while True:
            curr_ts = time.monotonic()
            if len(self._times) < self._rate_limit:
                break

            diff = curr_ts - (self._times[-1] + self._period)
            if diff > 0.:
                self._times.pop()
                break
            await asyncio.sleep(diff)

        self._times.appendleft(curr_ts)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

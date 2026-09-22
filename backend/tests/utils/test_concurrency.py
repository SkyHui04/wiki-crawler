import asyncio
import time

import pytest

from app.utils.concurrency import ConcurrentTaskManager

_SLEEP_MULTIPLIER = 0.05
_ACCEPTABLE_LATENCY_PCT = 0.25


class DummyConcurrentTaskManager(ConcurrentTaskManager[int, float]):
    @staticmethod
    def run_sync(parameter: int) -> float:
        result = _SLEEP_MULTIPLIER * parameter
        time.sleep(result)
        return result


class Timer:
    _start: float
    _stop: float
    _duration: float

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._stop = time.perf_counter()
        self._duration = self._stop - self._start

    @property
    def duration(self) -> float:
        return self._duration


@pytest.mark.asyncio
async def test_ctm_single_threaded():
    with DummyConcurrentTaskManager(1) as ctm, Timer() as timer:
        async with asyncio.timeout(_SLEEP_MULTIPLIER * 50):
            await asyncio.gather(*[ctm.assign_and_run(1) for _ in range(20)])

    expected_duration = _SLEEP_MULTIPLIER * 20

    print(f"expected duration: {expected_duration}")
    print(f"actual duration: {timer.duration}")

    assert timer.duration < expected_duration * (1.0 + _ACCEPTABLE_LATENCY_PCT)


@pytest.mark.asyncio
async def test_ctm_multi_threaded():
    with DummyConcurrentTaskManager(4) as ctm, Timer() as timer:
        async with asyncio.timeout(_SLEEP_MULTIPLIER * 50):
            await asyncio.gather(*[ctm.assign_and_run(1) for _ in range(20)])

    expected_duration = _SLEEP_MULTIPLIER * 20 / 4

    print(f"expected duration: {expected_duration}")
    print(f"actual duration: {timer.duration}")

    assert timer.duration < expected_duration * (1.0 + _ACCEPTABLE_LATENCY_PCT)

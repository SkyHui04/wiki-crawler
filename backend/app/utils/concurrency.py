import asyncio
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Self


class ConcurrentTaskManager[ParamT, ReturnT](ABC):
    num_threads: int

    def __init__(self, num_threads: int) -> None:
        if num_threads < 1:
            raise ValueError("num_threads must be at least 1")

        self.num_threads = num_threads
        self._executor: ThreadPoolExecutor | None = None
        self._lock = Lock()

    def start(self) -> None:
        """Create the thread pool."""
        with self._lock:
            if self._executor is not None:
                raise RuntimeError("Task manager is already started")

            self._executor = ThreadPoolExecutor(
                max_workers=self.num_threads,
                thread_name_prefix=type(self).__name__,
            )

    def stop(self) -> None:
        """Wait for submitted tasks and clean up the thread pool."""
        with self._lock:
            executor = self._executor
            self._executor = None

        if executor is not None:
            executor.shutdown(wait=True)

    @staticmethod
    @abstractmethod
    def run_sync(parameter: ParamT) -> ReturnT:
        """Process one parameter."""
        raise NotImplementedError

    async def assign_and_run(self, parameter: ParamT) -> ReturnT:
        """
        Submit one task to the pool and return its result.

        If all worker threads are busy, the task waits in the executor's
        internal queue until a worker becomes available.
        """
        with self._lock:
            executor = self._executor

        if executor is None:
            raise RuntimeError("Task manager has not been started")

        return await asyncio.wrap_future(executor.submit(self.run_sync, parameter))

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

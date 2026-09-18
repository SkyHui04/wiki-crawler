from collections import deque


class Stack[T]:
    _capacity: int | None
    _items: deque[T]

    def __init__(
        self, items: list[T] | None = None, capacity: int | None = None
    ) -> None:
        self._items = deque(items or [], capacity)
        self._capacity = capacity

    @property
    def capacity(self) -> int | None:
        return self._capacity

    @property
    def size(self) -> int:
        return len(self._items)

    def __len__(self) -> int:
        return self.size

    def push(self, item: T):
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def push_multi(self, items: list[T]):
        self._items.extend(items)

    def pop_multi(self, max_count: int | None = None) -> list[T]:
        if max_count is None:
            max_count = len(self._items)

        max_count = min(max_count, len(self._items))

        return [self._items.pop() for _ in range(max_count)]

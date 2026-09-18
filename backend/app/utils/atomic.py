from dataclasses import dataclass, field


@dataclass
class AtomicCounter:
    _value: int = field(default=0, repr=False)

    def increment(self) -> int:
        """Guaranteed consistency on single-OS-thread operations."""
        curr = self._value
        self._value += 1
        return curr

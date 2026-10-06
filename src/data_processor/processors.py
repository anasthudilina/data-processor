"""Pure data-processing functions: search, filter, group, sort."""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from collections.abc import Callable, Iterable

from .decorators import measure_time


# ---------------------------------------------------------------- comprehensions
def get_unique_types(accounts: list[dict]) -> set[str]:
    """Set comprehension — unique account types."""
    return {a["type"] for a in accounts}


def get_unique_clients(accounts: list[dict]) -> set[str]:
    return {a["client"] for a in accounts}


def create_account_index(accounts: list[dict]) -> dict[str, dict]:
    """Dict comprehension — account_number -> account (O(1) lookup)."""
    return {a["account_number"]: a for a in accounts}


def create_id_index(accounts: list[dict]) -> dict[int, dict]:
    return {a["id"]: a for a in accounts}


# ---------------------------------------------------------------- filtering
def filter_by_type(accounts: list[dict], acc_type: str) -> list[dict]:
    """List comprehension — filter by account type."""
    return [a for a in accounts if a["type"] == acc_type]


def filter_by_min_balance(accounts: list[dict], minimum: float) -> list[dict]:
    return [a for a in accounts if a["balance"] >= minimum]


def filter_items(
    items: list[dict],
    predicate: Callable[[dict], bool],
) -> list[dict]:
    """Universal higher-order filter (works with lambda or closure)."""
    return [item for item in items if predicate(item)]


# ---------------------------------------------------------------- grouping
def group_by_type(accounts: list[dict]) -> dict[str, list[dict]]:
    """Grouping via `defaultdict(list)`."""
    grouped: defaultdict[str, list[dict]] = defaultdict(list)
    for a in accounts:
        grouped[a["type"]].append(a)
    return dict(grouped)


def group_by_field(
    items: list[dict],
    field: str,
) -> dict[str, list[dict]]:
    """Generic grouping by any key field."""
    grouped: defaultdict[str, list[dict]] = defaultdict(list)
    for item in items:
        grouped[item[field]].append(item)
    return dict(grouped)


# ---------------------------------------------------------------- counting
def count_accounts_by_type(accounts: list[dict]) -> Counter:
    """Counter — how many accounts of each type."""
    return Counter(a["type"] for a in accounts)


def count_accounts_by_currency(accounts: list[dict]) -> Counter:
    return Counter(a["currency"] for a in accounts)


# ---------------------------------------------------------------- search
def search_account_linear(accounts: list[dict], account_number: str) -> dict | None:
    """O(n) linear search in a list."""
    for a in accounts:
        if a["account_number"] == account_number:
            return a
    return None


def search_account_by_index(index: dict[str, dict], account_number: str) -> dict | None:
    """O(1) average search in a dict index."""
    return index.get(account_number)


# ---------------------------------------------------------------- sorting
def sort_items(
    items: Iterable[dict],
    key: Callable[[dict], object],
    reverse: bool = False,
) -> list[dict]:
    """Universal sort with a higher-order key function."""
    return sorted(items, key=key, reverse=reverse)


# ---------------------------------------------------------------- pipeline
def pipeline(data, *steps):
    """Apply each step (callable) to the data sequentially."""
    result = data
    for step in steps:
        result = step(result)
    return result


# ---------------------------------------------------------------- deque-based history
class OperationHistory:
    """Fixed-size history of the most recent operations (uses deque)."""

    def __init__(self, maxlen: int = 5) -> None:
        self._history: deque[str] = deque(maxlen=maxlen)

    def add(self, operation: str) -> None:
        self._history.append(operation)

    def last(self, n: int = 3) -> list[str]:
        return list(self._history)[-n:]

    def __len__(self) -> int:
        return len(self._history)

    def __iter__(self):
        return iter(self._history)
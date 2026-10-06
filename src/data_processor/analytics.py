"""Aggregation, statistics, closures, benchmarks."""

from __future__ import annotations

from collections.abc import Callable
from time import perf_counter

from .decorators import log_call, measure_time
from .processors import search_account_linear


# ---------------------------------------------------------------- aggregation
@measure_time
def calculate_total_balance(accounts: list[dict]) -> float:
    """Aggregation with generator expression — O(n)."""
    return sum(a["balance"] for a in accounts)


@measure_time
def calculate_average_balance(accounts: list[dict]) -> float:
    if not accounts:
        return 0.0
    return sum(a["balance"] for a in accounts) / len(accounts)


def find_richest_account(accounts: list[dict]) -> dict | None:
    """Account with max balance — O(n)."""
    if not accounts:
        return None
    return max(accounts, key=lambda a: a["balance"])


def find_poorest_account(accounts: list[dict]) -> dict | None:
    if not accounts:
        return None
    return min(accounts, key=lambda a: a["balance"])


def sort_by_balance(accounts: list[dict], reverse: bool = True) -> list[dict]:
    return sorted(accounts, key=lambda a: a["balance"], reverse=reverse)


def sort_by_client(accounts: list[dict]) -> list[dict]:
    return sorted(accounts, key=lambda a: a["client"])


def balance_by_type(accounts: list[dict]) -> dict[str, float]:
    """Total balance per account type (nested aggregation)."""
    buckets: dict[str, float] = {}
    for a in accounts:
        buckets[a["type"]] = buckets.get(a["type"], 0.0) + a["balance"]
    return buckets


def average_balance_by_type(accounts: list[dict]) -> dict[str, float]:
    buckets: dict[str, list[float]] = {}
    for a in accounts:
        buckets.setdefault(a["type"], []).append(a["balance"])
    return {t: sum(v) / len(v) for t, v in buckets.items()}


def balance_statistics(accounts: list[dict]) -> dict:
    balances = [a["balance"] for a in accounts]
    if not balances:
        return {"count": 0, "min": 0.0, "max": 0.0, "total": 0.0, "average": 0.0}
    return {
        "count": len(balances),
        "min": min(balances),
        "max": max(balances),
        "total": sum(balances),
        "average": sum(balances) / len(balances),
    }


# ---------------------------------------------------------------- *args / **kwargs
def calculate_average_values(*values: float) -> float:
    """*args — variable number of positional arguments."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def create_record(**fields) -> dict:
    """**kwargs — build a dict from arbitrary keyword arguments."""
    return dict(fields)


# ---------------------------------------------------------------- closures
def create_min_balance_filter(minimum: float) -> Callable[[dict], bool]:
    """Closure: returned predicate remembers `minimum`."""
    def predicate(account: dict) -> bool:
        return account["balance"] >= minimum
    return predicate


def create_balance_range_filter(minimum: float, maximum: float) -> Callable[[dict], bool]:
    """Closure with two captured variables."""
    def predicate(account: dict) -> bool:
        return minimum <= account["balance"] <= maximum
    return predicate


# ---------------------------------------------------------------- benchmark
def benchmark_search(
    n_records: int,
    n_queries: int,
    dataset_factory,
) -> dict[str, float]:
    """Compare linear list search vs dict-index search.

    Complexity:
      - index build : O(n)
      - linear      : O(n) per query
      - dict        : O(1) average per query
    """
    accounts = dataset_factory(n_records)
    query_numbers = [a["account_number"] for a in accounts[:n_queries]]

    # build index
    t0 = perf_counter()
    index = {a["account_number"]: a for a in accounts}
    build_time = perf_counter() - t0

    # linear search
    t0 = perf_counter()
    for num in query_numbers:
        search_account_linear(accounts, num)
    linear_time = perf_counter() - t0

    # dict search
    t0 = perf_counter()
    for num in query_numbers:
        index.get(num)
    dict_time = perf_counter() - t0

    return {
        "records": n_records,
        "queries": n_queries,
        "index_build": build_time,
        "linear_search": linear_time,
        "dict_search": dict_time,
    }


@log_call
def demo_logged_summary(accounts: list[dict]) -> dict:
    return balance_statistics(accounts)
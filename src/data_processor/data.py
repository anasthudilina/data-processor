"""Structured input data for Variant 4 — banking accounts system."""

from __future__ import annotations

# ---------- tuple: immutable set of supported account types ----------
ACCOUNT_TYPES: tuple[str, ...] = (
    "current",
    "savings",
    "deposit",
    "credit",
)

# ---------- set: unique currencies in use ----------
CURRENCIES: set[str] = {"UAH", "USD", "EUR"}

# ---------- list of dicts: main structured dataset ----------
accounts: list[dict] = [
    {"id": 1,  "client": "Anna Koval",        "account_number": "UA0100001", "balance": 15230.50, "type": "current", "currency": "UAH"},
    {"id": 2,  "client": "Oleh Melnyk",       "account_number": "UA0100002", "balance": 84000.00, "type": "savings", "currency": "UAH"},
    {"id": 3,  "client": "Iryna Bondar",      "account_number": "UA0100003", "balance": 250000.75, "type": "deposit", "currency": "USD"},
    {"id": 4,  "client": "Andrii Shevchenko", "account_number": "UA0100004", "balance": 3120.10,  "type": "current", "currency": "UAH"},
    {"id": 5,  "client": "Maria Boyko",       "account_number": "UA0100005", "balance": 4300.00,  "type": "credit",  "currency": "UAH"},
    {"id": 6,  "client": "Taras Novak",       "account_number": "UA0100006", "balance": 98000.00, "type": "savings", "currency": "EUR"},
    {"id": 7,  "client": "Olena Hrytsenko",   "account_number": "UA0100007", "balance": 15600.00, "type": "current", "currency": "UAH"},
    {"id": 8,  "client": "Petro Sydorenko",   "account_number": "UA0100008", "balance": 720.45,   "type": "credit",  "currency": "UAH"},
    {"id": 9,  "client": "Yulia Marchenko",   "account_number": "UA0100009", "balance": 320000.00, "type": "deposit", "currency": "USD"},
    {"id": 10, "client": "Dmytro Tkachenko",  "account_number": "UA0100010", "balance": 45100.80, "type": "savings", "currency": "UAH"},
]


def generate_accounts(n: int) -> list[dict]:
    """Generate a synthetic dataset for benchmarking.

    Uses list comprehension; type/currency chosen from tuples/sets.
    """
    import random

    currency_list = list(CURRENCIES)
    return [
        {
            "id": i,
            "client": f"Client_{i}",
            "account_number": f"UA{1_000_000 + i:07d}",
            "balance": round(random.uniform(100.0, 500_000.0), 2),
            "type": ACCOUNT_TYPES[i % len(ACCOUNT_TYPES)],
            "currency": currency_list[i % len(currency_list)],
        }
        for i in range(1, n + 1)
    ]
"""Entry point — runs the full demo of Lab 02 (Variant 4)."""

from __future__ import annotations

from .analytics import (
    average_balance_by_type,
    balance_by_type,
    balance_statistics,
    benchmark_search,
    calculate_average_balance,
    calculate_average_values,
    calculate_total_balance,
    create_balance_range_filter,
    create_min_balance_filter,
    create_record,
    demo_logged_summary,
    find_poorest_account,
    find_richest_account,
    sort_by_balance,
    sort_by_client,
)
from .data import ACCOUNT_TYPES, CURRENCIES, accounts, generate_accounts
from .decorators import repeat
from .processors import (
    OperationHistory,
    count_accounts_by_currency,
    count_accounts_by_type,
    create_account_index,
    create_id_index,
    filter_by_min_balance,
    filter_by_type,
    filter_items,
    get_unique_clients,
    get_unique_types,
    group_by_field,
    group_by_type,
    pipeline,
    search_account_by_index,
    search_account_linear,
    sort_items,
)


# ------------------------------------------------------------------ helpers
def print_accounts(title: str, items: list[dict]) -> None:
    print(f"\n{title}")
    print("-" * 78)
    print(f"{'id':>3}  {'client':<22} {'account':<12} {'type':<8} "
          f"{'currency':<8} {'balance':>12}")
    print("-" * 78)
    for a in items:
        print(f"{a['id']:>3}  {a['client']:<22} {a['account_number']:<12} "
              f"{a['type']:<8} {a['currency']:<8} {a['balance']:>12.2f}")


def print_section(title: str) -> None:
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


# ------------------------------------------------------------------ demo steps
@repeat(2)
def show_processing_banner() -> None:
    print("  [repeat-decorator] banking data processing...")


def demo_builtin_structures() -> None:
    print_section("1) Built-in structures: list / tuple / set / dict")
    print("ACCOUNT_TYPES (tuple)  :", ACCOUNT_TYPES)
    print("CURRENCIES (set)       :", CURRENCIES)
    print("accounts (list) len    :", len(accounts))
    print("sample dict            :", accounts[0])


def demo_comprehensions() -> None:
    print_section("2) Comprehensions")
    print("set comprehension  — unique types     :", get_unique_types(accounts))
    print("set comprehension  — unique clients   :", get_unique_clients(accounts))
    print("dict comprehension — account index sz :", len(create_account_index(accounts)))
    print("dict comprehension — id index sz      :", len(create_id_index(accounts)))
    print("list comprehension — current accounts :",
          [a["id"] for a in filter_by_type(accounts, "current")])


def demo_collections() -> None:
    print_section("3) collections: Counter / defaultdict / deque")
    counter_type = count_accounts_by_type(accounts)
    counter_cur = count_accounts_by_currency(accounts)
    print("Counter by type         :", dict(counter_type))
    print("Counter by currency     :", dict(counter_cur))

    grouped = group_by_type(accounts)
    print("defaultdict grouping    :",
          {t: len(members) for t, members in grouped.items()})

    history = OperationHistory(maxlen=4)
    history.add("load")
    history.add("filter")
    history.add("group")
    history.add("sort")
    history.add("benchmark")
    print("deque history (last 3)  :", history.last(3))


def demo_search() -> None:
    print_section("4) Search: linear vs dict index (by account_number)")
    index = create_account_index(accounts)

    target = "UA0100003"
    print(f"linear -> {target}:", search_account_linear(accounts, target))
    print(f"index  -> {target}:", search_account_by_index(index, target))
    print(f"index  -> UA9999999:", search_account_by_index(index, "UA9999999"))


def demo_sorting() -> None:
    print_section("5) Sorting — lambda / higher-order key")
    print_accounts("Ranking by balance (desc):", sort_by_balance(accounts))
    print_accounts("Sorted by client        :", sort_by_client(accounts))
    print_accounts("Universal sort (balance):",
                   sort_items(accounts, key=lambda a: a["balance"]))


def demo_grouping_and_stats() -> None:
    print_section("6) Grouping, aggregation, statistics")
    grouped = group_by_field(accounts, "type")
    for t, members in grouped.items():
        avg = sum(m["balance"] for m in members) / len(members)
        print(f"  {t:<8}: {len(members)} accounts, average = {avg:.2f}")

    print("\nTotal balance by type        :", balance_by_type(accounts))
    print("Average balance by type      :",
          {k: round(v, 2) for k, v in average_balance_by_type(accounts).items()})
    print("Statistics                   :", balance_statistics(accounts))
    print("Richest account              :",
          find_richest_account(accounts)["client"],
          find_richest_account(accounts)["balance"])
    print("Poorest account              :",
          find_poorest_account(accounts)["client"],
          find_poorest_account(accounts)["balance"])
    print("Total balance (decorated)    :",
          round(calculate_total_balance(accounts), 2))
    print("Average balance (decorated)  :",
          round(calculate_average_balance(accounts), 2))


def demo_closures_and_higher_order() -> None:
    print_section("7) Closures + higher-order filtering")
    is_rich = create_min_balance_filter(50_000.0)
    in_range = create_balance_range_filter(1_000.0, 100_000.0)

    print("balance >= 50000     :",
          [a["account_number"] for a in filter_items(accounts, is_rich)])
    print("1000 <= balance <= 100000:",
          [a["account_number"] for a in filter_items(accounts, in_range)])


def demo_args_kwargs() -> None:
    print_section("8) *args / **kwargs")
    demo_avg = calculate_average_values(15230.50, 84000.0, 250000.75, 3120.10)
    print("average via *args  :", round(demo_avg, 2))

    new_account = create_record(
        id=11, client="Bohdan Levchenko",
        account_number="UA0100011",
        balance=25000.0, type="current", currency="UAH",
    )
    print("record via **kwargs:", new_account)


def demo_pipeline() -> None:
    print_section("9) Pipeline processing")
    result = pipeline(
        accounts,
        lambda data: filter_by_min_balance(data, 20_000.0),
        group_by_type,
    )
    print("pipeline(balance>=20000 → group by type):",
          {t: len(v) for t, v in result.items()})


def demo_benchmark() -> None:
    print_section("10) Benchmark: list search vs dict search")
    print(f"{'records':>8} | {'queries':>7} | {'index build':>12} | "
          f"{'linear':>12} | {'dict':>12}")
    print("-" * 68)

    for n in (500, 5_000, 20_000):
        res = benchmark_search(n, 200, generate_accounts)
        print(f"{res['records']:>8} | {res['queries']:>7} | "
              f"{res['index_build']:>12.6f} | "
              f"{res['linear_search']:>12.6f} | "
              f"{res['dict_search']:>12.6f}")


# ------------------------------------------------------------------ entry point
def main() -> None:
    print_section("LAB 02 — Banking accounts analysis (Variant 4)")
    show_processing_banner()

    demo_builtin_structures()
    demo_comprehensions()
    demo_collections()
    demo_search()
    demo_sorting()
    demo_grouping_and_stats()
    demo_closures_and_higher_order()
    demo_args_kwargs()
    demo_pipeline()
    demo_benchmark()

    demo_logged_summary(accounts)


if __name__ == "__main__":
    main()
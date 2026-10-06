"""Decorators used throughout the module."""

from functools import wraps
from time import perf_counter


def log_call(func):
    """Log function entry and exit without touching its body."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG ] -> {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG ] <- {func.__name__}")
        return result
    return wrapper


def measure_time(func):
    """Measure execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"[TIME] {func.__name__}: {elapsed:.8f} s")
        return result
    return wrapper


def repeat(count: int):
    """Parameterized decorator — calls the wrapped function `count` times.

    Demonstrates: decorator + closure + *args + **kwargs.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(count):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
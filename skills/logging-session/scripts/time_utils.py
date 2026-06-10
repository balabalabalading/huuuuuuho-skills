"""Shared time utilities. All timestamps use the system's local timezone."""
from datetime import datetime, timedelta


def local_now_str() -> str:
    """Return current local time as a naive 'YYYY-MM-DD HH:MM:SS' string.

    Uses the operating system's local timezone. Naive strings are used for
    SQLite storage because SQLite has no timezone support. All query
    boundaries must also be computed Python-side to stay consistent.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def local_date_str(days_ago: int = 0) -> str:
    """Return local-time date string 'YYYY-MM-DD' for N days ago.

    days_ago=0 → today, days_ago=1 → yesterday, etc.
    """
    dt = datetime.now() - timedelta(days=days_ago)
    return dt.strftime("%Y-%m-%d")


def local_day_start_str(days_ago: int = 0) -> str:
    """Return 'YYYY-MM-DD HH:MM:SS' at midnight local time N days ago.

    Used as a query boundary to replace SQLite's datetime('now', ...)
    which returns UTC on SQLite ≥ 3.38 and is inconsistent across versions.
    """
    dt = datetime.now() - timedelta(days=days_ago)
    return dt.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")

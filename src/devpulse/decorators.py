import datetime
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def start_time_stamp[**P, T](function: Callable[P, T]) -> Callable[P, tuple[T, datetime.datetime]]:
    @wraps(function)
    def wrapper(*args, **kwargs):
        observed_at = datetime.datetime.now(datetime.UTC)
        result = function(*args, **kwargs)
        return result, observed_at
    return wrapper

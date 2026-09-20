import datetime
from functools import wraps


def start_time_stamp(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        observed_at = datetime.datetime.now(datetime.UTC)
        result = function(*args, **kwargs)
        return result, observed_at
    return wrapper

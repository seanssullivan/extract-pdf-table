# helpers/decorators.py

import logging
import time


def log_time(func: function) -> function:
    """Decorator for logging function execution time."""

    def timed_function(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time

        logging.info(f"{func.__name__} took {elapsed_time:0.4f} to execute.")
        return result

    return timed_function

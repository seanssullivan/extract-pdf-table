# helpers/comparators.py

# Standard Imports
from typing import Literal


def within_margin(actual: int, expected: int, margin: int) -> bool:
    return True if actual <= expected + margin and actual >= expected - margin else False


def within_proximity(current: dict, other: dict, margin: int = 0, axis: Literal[0, 1] = None) -> bool:

    if (axis is None or axis != 1) \
        and (current['top'] > other['bottom'] + margin \
        or current['bottom'] < other['top'] - margin):
        return False
    
    if (axis is None or axis != 0) \
        and current['left'] > other['right'] + margin \
        and current['right'] < other['left'] - margin:
        return False

    if (axis == 0) \
        and (current['right'] + current['left']) / 2 > other['right'] \
        and (other['right'] + other['left']) / 2 < current['left']:
        return False

    if (axis == 0) \
        and (current['right'] + current['left']) / 2 < other['left'] \
        and (other['right'] + other['left']) / 2 > current['right']:
        return False

    if (axis == 1) \
        and (current['top'] + current['bottom']) / 2 > other['bottom'] \
        and (other['top'] + other['bottom']) / 2 < current['top']:
        return False
    
    if (axis == 1) \
        and (current['top'] + current['bottom']) / 2 < other['top'] \
        and (other['top'] + other['bottom']) / 2 > current['bottom']:
        return False
    
    return True

# src/parser/callbacks/length.py

# Standard Imports
from typing import Iterable, Union

# Third-Party Imports
from pdfminer.layout import LTComponent


def equals(length: int) -> bool:
    """
    Returns a callback function which checks whether an element is the provided length.
    :param length: number of components the element should contain.
    :returns: a callback function.
    """

    def callback(element: Union[Iterable, LTComponent]):
        """Checks whether an element is the provided length."""
        return len(element) == length

    return callback


def greater_than(length: int) -> bool:
    """
    Returns a callback function which checks whether an element is greater than the provided length.
    :param length: number of components the element should contain more than.
    :returns: a callback function.
    """

    def callback(element: Union[Iterable, LTComponent]):
        """Checks whether an element is greater than the provided length."""
        return len(element) > length

    return callback


def less_than(length: int) -> bool:
    """
    Returns a callback function which checks whether an element is less than the provided length.
    :param length: number of components the element should contain less than.
    :returns: a callback function.
    """

    def callback(element: Union[Iterable, LTComponent]):
        """Checks whether an element is less than the provided length."""
        return len(element) < length

    return callback

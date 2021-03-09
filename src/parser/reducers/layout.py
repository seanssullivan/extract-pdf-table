# src/parser/reducers/layout.py

# Standard Imports
from typing import Callable, Iterable, List, Set, Tuple, Union

# Third-Party Imports
from pdfminer.layout import LTItem

# Local Imports
from ..abstractors import get_position


def reduce_positions(
    accumulator: Union[List, Set],
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[Tuple]:
    """
    Return the positions of all objects in a container.
    :param accumulator: an instance of list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the items.
    """
    # Extract the positions of all objects
    positions = [
        get_position(obj)
        for obj in container
        if all(map(lambda cb: cb(obj), callbacks))
    ]
    # return accumulated values
    return _accumulate(accumulator, positions)


def _accumulate(accumulator: Union[List, Set], items: List) -> Union[List, Set]:
    """Add items to the accumulator."""
    # if accumulator is a list, return the entire list
    if isinstance(accumulator, List):
        return items

    # if accumulator is a set, add items to set
    elif isinstance(accumulator, Set):
        return set(items)

    # else accumulator is not a valid type
    else:
        raise TypeError("accumulator must be list or set")

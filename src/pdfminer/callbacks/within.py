# src/pdfminer/callbacks/within.py

# Standard Imports
from operator import attrgetter
from typing import Tuple, Union

# Third-Party Imports
from pdfminer.layout import LTItem


def within(boundary: Tuple = None, margin: float = 0) -> bool:
    """
    Returns a callback function that checks whether a layout item is within a given boundary.

    :param boundary: tuple containing left, bottom, right and top positions of a bounding box.
    :param margin: optional margin of error.
    :returns: a callback function.
    """
    if boundary and len(boundary) != 4:
        raise ValueError

    def callback(item: Union[LTItem, Tuple]):
        """
        A callback function that checks a layout item against a provided boundary.
        :param item: either a LTItem layout component or a tuple of its position.
        :returns: whether the item is within the boundary.
        """
        if not boundary:
            return True

        if isinstance(item, Tuple):
            bbox = item
        elif all(map(lambda attr: hasattr(item, attr), ['x0', 'y0', 'x1', 'y1'])):
            bbox = attrgetter('x0', 'y0', 'x1', 'y1')(item)
        else:
            raise ValueError(f"{item!s} is not a valid argument type")

        return (
            bbox[0] >= boundary[0] - margin and  # left side
            bbox[1] >= boundary[1] - margin and  # bottom side
            bbox[2] <= boundary[2] + margin and  # right side
            bbox[3] <= boundary[3] + margin      # top side
        )

    return callback

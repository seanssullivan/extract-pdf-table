# src/pdfminer/callbacks/between.py

# Standard Imports
from operator import attrgetter
from typing import Tuple

# Third-Party Imports
from pdfminer.layout import LTComponent


def between(boundary: Tuple = None, axis: int = 1, margin: int = 0) -> bool:
    """
    Returns a callback function that checks whether a layout item is entirely between two boundaries.
    :param boundary: tuple containing two positions (left and right, or bottom and top).
    :param axis: integer representing either a vertical (0) or a horizontal (1) axis.
    :param margin: optional margin of error.
    :returns: a callback function.
    """
    if boundary and len(boundary) != 2:
        raise ValueError

    def callback(item: LTComponent):
        """Checks layout item against horizontal boundaries."""
        if not boundary:
            return True

        if isinstance(item, Tuple):
            bbox = item

        elif all(map(lambda attr: hasattr(item, attr), ['x0', 'y0', 'x1', 'y1'])):
            if axis == 1:
                bbox = attrgetter('x0', 'x1')(item) # left and right
            else:
                bbox = attrgetter('y0', 'y1')(item) # bottom and top

        else:
            raise ValueError(f"{item!s} is not a valid argument type")

        return (
            bbox[0] >= boundary[0] - margin and  # left or bottom
            bbox[1] <= boundary[1] + margin      # right or top
        )

    return callback

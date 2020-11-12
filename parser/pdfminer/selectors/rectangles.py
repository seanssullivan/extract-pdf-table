# parsers/pdfminer/selectors/rectangles.py

# Standard Imports
from typing import Callable, Iterable, Iterator

# Third-Party Imports
from pdfminer.layout import LTItem, LTPage, LTRect, LTTextContainer


def select_rectangles(
    container: Iterable,
    *callbacks: Callable
    ) -> Iterator[LTRect]:
    """Select instances of LTRect objects."""

    # If argument is not an instance of an LTItem and not iterable, it is not an appropriate argument type
    if not isinstance(container, LTItem) and not isinstance(container, Iterable):
        raise TypeError(f"{type(container)} is not a valid argument type")

    # If argument is an instance of an LTTextContainer, it will not contain rectangles
    # Therefore return an empty list
    if isinstance(container, LTTextContainer):
        return []

    # if argument is a single LTRect object, return it
    if isinstance(container, LTRect):
        return [container] if all(map(lambda cb: cb(container), callbacks)) else []

    rectangles = []
    # ensure argument is an LTPage object, then yield rectangles
    if isinstance(container, LTPage):
        rectangles.extend(_rectangles_from_page(container, *callbacks))

    # check whether the object is iterable and may yield either pages or rectangles
    elif isinstance(container, Iterable):
        rectangles.extend([
            rectangle
            for element in container
            for rectangle in select_rectangles(element, *callbacks)
        ])
    
    # otherwise return an empty list
    else:
        pass
    
    return rectangles


def _rectangles_from_page(page: LTPage, *callbacks: Callable):
    """Select instances of LTRect from a LTPage object.

    This function is designed to help select instances of LTRect objects
    and should not be imported into other modules."""
    return [
        rectangle
        for rectangle in page
        if isinstance(rectangle, LTRect)
        and all(map(lambda cb: cb(rectangle), callbacks)) 
    ]

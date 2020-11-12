# parsers/pdfminer/selectors/pages.py

# Standard Imports
from typing import Callable, Iterable, Iterator, Union

# Third-Party Imports
from pdfminer.layout import LTComponent, LTCurve, LTPage


def select_pages(
    container: Union[Iterable[LTPage], LTPage],
    *callbacks: Callable
    ) -> Iterator[LTPage]:
    """Select instances of LTPage objects."""

    # If argument is not an instance of an LTComponent and not iterable, it is not an appropriate argument type
    if not isinstance(container, LTComponent) and not isinstance(container, Iterable):
        raise TypeError(f"{type(container)} is not a valid argument type")

    # If argument is an instance of an LTCurve, it will not contain text
    # Therefore return an empty list
    if isinstance(container, LTCurve):
        return []

    # if argument is a single LTPage object, return it
    if isinstance(container, LTPage):
        return (
            [container]
            if all(map(lambda cb: cb(container), callbacks))
            else []
        )

    pages = []
    # check whether argument is iterable, then yield pages
    if isinstance(container, Iterable):
        pages.extend(_pages_from_iterable(container, *callbacks))
    
    # otherwise return an empty list
    else:
        pass

    return pages


def _pages_from_iterable(container: Iterable, *callbacks: Callable):
    """Select instances of LTPage objects from an iterable object.

    This function is designed to help select instances of LTPage objects
    and should not be imported into other modules."""
    return [
        page for page in container
        if isinstance(page, LTPage) 
        and all(map(lambda cb: cb(page), callbacks))
    ]

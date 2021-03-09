# parsers/pdfminer/selectors/lines.py

# Standard Imports
from typing import Callable, Iterable, Iterator, Union

# Third-Party Imports
from pdfminer.layout import LTComponent, LTCurve, LTPage, LTTextBox, LTTextLine

# Local Imports
from .textboxes import select_textboxes


def select_lines(
    container: Union[Iterable, LTComponent],
    *callbacks: Callable
    ) -> Iterator[LTTextLine]:
    """Select instances of LTTextLine objects."""

    # If argument is not an instance of an LTComponent and not iterable, it is not an appropriate argument type
    if not isinstance(container, LTComponent) and not isinstance(container, Iterable):
        raise TypeError(f"{type(container)} is not a valid argument type")

    # If argument is an instance of an LTCurve, it will not contain text
    # Therefore return an empty list
    if isinstance(container, LTCurve):
        return []

    # if argument is a single LTTextLine object, return it
    if isinstance(container, LTTextLine):
        return (
            [container]
            if all(map(lambda cb: cb(container), callbacks))
            else []
        )
    
    lines = []
    # ensure argument is an LTTextBox object, then yield lines of text
    if isinstance(container, LTTextBox):
        lines.extend(_lines_from_textbox(container, *callbacks))

    # for an LTPage object, retrieve the textboxes first
    elif isinstance(container, LTPage):
        lines.extend(_lines_from_page(container, *callbacks))

    # else if object is iterable, check for either pages, textboxes or lines
    elif isinstance(container, Iterable):
        lines.extend(_lines_from_iterable(container, *callbacks))

    # otherwise return an empty list
    else:
        pass

    return lines


def _lines_from_page(page: LTPage, *callbacks: Callable):
    """Select instances of LTTextLine from a LTPage object.

    This function is designed to help select instances of LTTextLine objects
    and should not be imported into other modules."""
    return [
        line
        for textbox in select_textboxes(page)
        for line in select_lines(textbox, *callbacks)
    ]


def _lines_from_textbox(textbox: LTTextBox, *callbacks: Callable):
    """Select instances of LTTextLine from a LTTextBox object.

    This function is designed to help select instances of LTTextLine objects
    and should not be imported into other modules."""
    return [
        line
        for line in textbox
        if isinstance(line, LTTextLine)
        and all(map(lambda cb: cb(line), callbacks))
    ]


def _lines_from_iterable(container: Iterable, *callbacks: Callable):
    """Select instances of LTTextLine from an iterable object.

    This function is designed to help select instances of LTTextLine objects
    and should not be imported into other modules."""
    return [
        line
        for element in container
        for line in select_lines(element, *callbacks)
    ]

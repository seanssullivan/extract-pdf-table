# parsers/pdfminer/selectors/characters.py

# Standard Imports
from typing import Callable, Iterable, Iterator, Union

# Third-Party Imports
from pdfminer.layout import LTComponent, LTCurve, LTPage, LTTextBox, LTTextLine, LTChar

# Local Imports
from .lines import select_lines
from .textboxes import select_textboxes


def select_characters(
    container: Union[Iterable, LTComponent],
    *callbacks: Callable
    ) -> Iterator[LTChar]:
    """Select instances of LTChar objects."""

    # If argument is not an instance of an LTComponent and not iterable, it is not an appropriate argument type
    if not isinstance(container, LTComponent) and not isinstance(container, Iterable):
        raise TypeError(f"{type(container)} is not a valid argument type")

    # If argument is an instance of an LTCurve, it will not contain text
    # Therefore return an empty list
    if isinstance(container, LTCurve):
        return []

    # if argument is a single LTChar object, return it
    if isinstance(container, LTChar):
        return (
            [container]
            if all(map(lambda cb: cb(container), callbacks))
            else []
        )
    
    characters = []
    # ensure argument is an LTTextLine object, then yield characters
    if isinstance(container, LTTextLine):
        characters.extend(_characters_from_line(container, *callbacks))
    
    # for LTTextBox objects, retrieve the lines first
    elif isinstance(container, LTTextBox):
        characters.extend(_characters_from_textbox(container, *callbacks))
    
    # for LTPage objects, retrieve the textboxes first
    elif isinstance(container, LTPage):
        characters.extend(_characters_from_page(container, *callbacks))

    # check whether the object is iterable and may yield pages, textboxes, lines or characters
    elif isinstance(container, Iterable):
        characters.extend(_characters_from_iterable(container, *callbacks))

    # otherwise return an empty list
    else:
        pass

    return characters


def _characters_from_page(page: LTPage, *callbacks: Callable):
    """Select instances of LTChar from a LTPage object.

    This function is designed to help select instances of LTChar objects
    and should not be imported into other modules."""
    return [
        char
        for textbox in select_textboxes(page)
        for char in select_characters(textbox, *callbacks)
    ]


def _characters_from_textbox(textbox: LTTextBox, *callbacks: Callable):
    """Select instances of LTChar from a LTTextBox object.

    This function is designed to help select instances of LTChar objects
    and should not be imported into other modules."""
    return [
        char
        for line in select_lines(textbox)
        for char in select_characters(line, *callbacks)
    ]


def _characters_from_line(line: LTTextLine, *callbacks: Callable):
    """Select instances of LTChar from a LTTextLine object.

    This function is designed to help select instances of LTChar objects
    and should not be imported into other modules."""
    return [
        char
        for char in line
        if isinstance(char, LTChar)
        and all(map(lambda cb: cb(char), callbacks))
    ]


def _characters_from_iterable(container: Iterable, *callbacks: Callable):
    """Select instances of LTChar from an iterable object.

    This function is designed to help select instances of LTChar objects
    and should not be imported into other modules."""
    return [
        char
        for element in container
        for char in select_characters(element, *callbacks)
    ]

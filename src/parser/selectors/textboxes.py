# parsers/pdfminer/selectors/textboxes.py

# Standard Imports
from typing import Callable, Iterable, Iterator, Union

# Third-Party Imports
from pdfminer.layout import LTCurve, LTItem, LTPage, LTTextBox


def select_textboxes(
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterator[LTTextBox]:
    """Select instances of LTTextBox objects."""

    # If argument is not an instance of an LTItem and not iterable, it is not an appropriate argument type
    if not isinstance(container, LTItem) and not isinstance(container, Iterable):
        raise TypeError(f"{type(container)} is not a valid argument type")

    # If argument is an instance of an LTCurve, it will not contain text
    # Therefore return an empty list
    if isinstance(container, LTCurve):
        return []

    # if argument is a single LTTextBox object, return it
    if isinstance(container, LTTextBox):
        return [container] if all(map(lambda cb: cb(container), callbacks)) else []

    textboxes = []
    # ensure argument is an LTPage object, then yield textboxes
    if isinstance(container, LTPage):
        textboxes.extend(_textboxes_from_page(container, *callbacks))        

    # else if object is iterable, check for either pages or textboxes
    elif isinstance(container, Iterable):
        textboxes.extend([
            textbox
            for element in container
            for textbox in select_textboxes(element, *callbacks)
        ])

    # otherwise return an empty list
    else:
        pass

    return textboxes


def _textboxes_from_page(page: LTPage, *callbacks: Callable):
    """Select instances of LTTextBox from a LTPage object.

    This function is designed to help select instances of LTTextBox objects
    and should not be imported into other modules."""
    return [
        textbox
        for textbox in page
        if isinstance(textbox, LTTextBox)
        and all(map(lambda cb: cb(textbox), callbacks)) 
    ]

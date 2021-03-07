# src/pdfminer/callbacks/text/equals.py

# Standard Imports
from typing import List, Text, Union

# Third-Party Imports
from pdfminer.layout import LTTextContainer


def equals(text: Text) -> bool:
    """
    Returns a callback function that checks whether an element's text equals the provided string.
    :param text: a string to check for.
    :returns: a callback function.
    """
    if not isinstance(text, Text):
        raise ValueError

    def callback(element: LTTextContainer):
        """Checks whether an element's text matches the provided text."""
        if hasattr(element, 'get_text'):
            return text == element.get_text().strip().replace('\n', '')
        else:
            raise TypeError

    return callback



def does_not_equal(text: Text) -> bool:
    """
    Returns a callback function that checks whether an element's text does not equal the provided string.
    :param text: a string to check for.
    :returns: a callback function.
    """
    if not isinstance(text, Text):
        raise ValueError

    def callback(element: LTTextContainer):
        """Checks whether an element's text does not match the provided text."""
        if hasattr(element, 'get_text'):
            return text != element.get_text().strip().replace('\n', '')
        else:
            raise TypeError

    return callback



def includes(*strings: Text) -> bool:
    """
    Returns a callback function that checks whether a containers's text includes the provided string(s).
    :param strings: strings to search for.
    :returns: a callback function.
    """
    def callback(container: LTTextContainer):
        """Checks whether an container includes the provided text."""
        if not hasattr(container, 'get_text'):
            raise TypeError

        text = container.get_text().strip().replace('\n', '')
        return all(map(lambda s: s in text, strings))

    return callback


def is_blank() -> bool:
    """
    Returns a callback function that checks whether an container's text is blank.
    :returns: a callback function.
    """
    return equals('')


def not_blank() -> bool:
    """
    Returns a callback function that checks whether a container's text is not blank.
    :returns: a callback function.
    """
    return does_not_equal('')

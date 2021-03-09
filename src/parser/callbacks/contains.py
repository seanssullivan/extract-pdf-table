# src/parser/callbacks/contains.py

# Standard Imports
from typing import Iterable, Type, Union

# Third-Party Imports
from pdfminer.layout import LTComponent


def contains(component: Union[LTComponent, Type]) -> bool:
    """
    Returns a callback function that checks whether a provided element contains another.
    :param component: an object to search for.
    :returns: a callback function.
    """

    def callback(element: Union[Iterable, LTComponent]):
        """Checks whether an element contains the provided component."""
        if isinstance(component, Type):
            return any(map(lambda obj: isinstance(obj, component), element))
        else:
            return component in element

    return callback

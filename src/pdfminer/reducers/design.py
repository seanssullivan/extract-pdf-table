# src/pdfminer/reducers/typography.py

# Standard Imports
from collections import Counter
from typing import Callable, Dict, Iterable, List, Set, Text, Union

# Third-Party Imports
from pdfminer.layout import LTItem

# Local Imports
from ..abstractors import get_fontname, get_fontsize, get_fontweight, get_typeface
from ..selectors import select_characters


def reduce_fontnames(
    accumulator: Union[Dict, List, Set],
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[Text]:
    """
    Return all font names used in a container.
    :param accumulator: an instance of dict, list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the LTChar items.
    """
    characters = select_characters(container)

    # extract fontnames from instances of LTChar
    fontnames = [
        get_fontname(char) for char in characters
        if all(map(lambda cb: cb(char), callbacks))
    ]

    # return accumulated values
    return _accumulate(accumulator, fontnames)


def reduce_fontsizes(
    accumulator: Union[Dict, List, Set],
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[int]:
    """
    Return all font sizes used in a container.
    :param accumulator: an instance of dict, list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the LTChar items.
    """
    characters = select_characters(container)

    # extract fontsizes from instances of LTChar
    fontsizes = [
        get_fontsize(char) for char in characters
        if all(map(lambda cb: cb(char), callbacks))
    ]

    # return accumulated values
    return _accumulate(accumulator, fontsizes)


def reduce_fontweights(
    accumulator: Union[Dict, List, Set],
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[Text]:
    """
    Return all font names used in a container.
    :param accumulator: an instance of dict, list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the LTChar items.
    """
    characters = select_characters(container)

    # extract fontweights from instances of LTChar
    fontweights = [
        get_fontweight(char) for char in characters
        if all(map(lambda cb: cb(char), callbacks))
    ]

    # return accumulated values
    return _accumulate(accumulator, fontweights)


def reduce_typefaces(
    accumulator: Union[Dict, List, Set],
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[Text]:
    """
    Return all typefaces used in a container.
    :param accumulator: an instance of dict, list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the LTChar items.
    """
    characters = select_characters(container)

    # extract typefaces from instances of LTChar
    typefaces = [
        get_typeface(char) for char in characters
        if all(map(lambda cb: cb(char), callbacks))
    ]

    # return accumulated values
    return _accumulate(accumulator, typefaces)


def _accumulate(accumulator: Union[Dict, List, Set], items: List) -> Union[Dict, List, Set]:
    """Add items to the accumulator."""
    # if accumulator is a dictionary, count the items
    if isinstance(accumulator, Dict):
        return Counter(items)

    # if accumulator is a list, return the entire list
    elif isinstance(accumulator, List):
        return items

    # if accumulator is a set, add itemds to set
    elif isinstance(accumulator, Set):
        return set(items)

    # else accumulator is not a valid type
    else:
        raise TypeError("accumulator must be dict, list or set")

# parser/pdfminer/reducers/typography.py

# Standard Imports
from typing import Callable, Dict, Iterable, List, Set, Text, Union

# Third-Party Imports
from pdfminer.layout import LTItem

# Local Imports
from parser.pdfminer.abstractors.fonts import get_fontname, get_fontsize, get_fontweight, get_typeface
from parser.pdfminer.selectors import select_characters


def reduce_fontnames(
    accumulator: Union[Dict, List, Set],
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[Text]:
    """
    Return all font names used in a container.
    :param accumulator: an instance of dict, list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the LTChar items before counting font names.
    """
    characters = select_characters(container)

    # extract fontnames from instances of LTChar
    fontnames = [
        get_fontname(char) for char in characters
        if all(map(lambda cb: cb(char), callbacks))
    ]
    _accumulate(accumulator, fontnames)
    return accumulator


def reduce_fontsizes(
    accumulator: Union[Dict, List, Set],
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[int]:
    """
    Return all font sizes used in a container.
    :param accumulator: an instance of dict, list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the LTChar items before counting font sizes.
    """
    characters = select_characters(container)

    # extract fontsizes from instances of LTChar
    fontsizes = [
        get_fontsize(char) for char in characters
        if all(map(lambda cb: cb(char), callbacks))
    ]
    _accumulate(accumulator, fontsizes)
    return accumulator


def reduce_fontweights(
    accumulator: Union[Dict, List, Set], 
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[Text]:
    """
    Return all font names used in a container.
    :param accumulator: an instance of dict, list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the LTChar items before counting font weights.
    """
    fontnames = reduce_fontnames([], container, *callbacks)

    # extract fontweights from instances of LTChar
    fontweights = [get_fontweight(fname) for fname in fontnames]

    _accumulate(accumulator, fontweights)
    return accumulator


def reduce_typefaces(
    accumulator: Union[Dict, List, Set],
    container: Union[Iterable, LTItem],
    *callbacks: Callable
    ) -> Iterable[Text]:
    """
    Return all typefaces used in a container.
    :param accumulator: an instance of dict, list or set.
    :param container: an instance of an LTItem object or an iterable containing them.
    :param callbacks: functions to filter the LTChar items before counting typefaces.
    """
    fontnames = reduce_fontnames([], container, *callbacks)

    # extract typefaces from instances of LTChar
    typefaces = [get_typeface(fname) for fname in fontnames]

    _accumulate(accumulator, typefaces)
    return accumulator


def _accumulate(accumulator: Union[Dict, List, Set], items: List) -> Union[Dict, List, Set]:
    """Add items to the accumulator."""
    # if accumulator is a dictionary, count the fontnames
    if isinstance(accumulator, Dict):
        for item in items:
            accumulator.setdefault(item, 0)
            accumulator[item] += 1

    # if accumulator is a list, return the entire list
    elif isinstance(accumulator, List):
        accumulator = items
    
    # if accumulator is a set, add fontnames to set
    elif isinstance(accumulator, Set):
        for item in items:
            accumulator.add(item)

    return accumulator

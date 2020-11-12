# parser/pdfminer/reducers/typography.py

# Standard Imports
from typing import Callable, Dict, Iterable, List, Set, Text, Union

# Third-Party Imports
from pdfminer.layout import LTItem

# Local Imports
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
        char.fontname.split('+')[1]
            if '+' in char.fontname
            else char.fontname
        for char in characters
        if all(map(lambda cb: cb(char), callbacks))
    ]

    # if accumulator is a dictionary, count the fontnames
    if isinstance(accumulator, Dict):
        for fontname in fontnames:
            accumulator.setdefault(fontname, 0)
            accumulator[fontname] += 1

    # if accumulator is a list, return the entire list
    elif isinstance(accumulator, List):
        accumulator = fontnames
    
    # if accumulator is a set, add fontnames to set
    elif isinstance(accumulator, Set):
        for fontname in fontnames:
            accumulator.add(fontname)

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
        char.size 
        for char in characters
        if all(map(lambda cb: cb(char), callbacks))
    ]

    # if accumulator is a dictionary, count the fontsizes
    if isinstance(accumulator, Dict):
        for fontsize in fontsizes:
            accumulator.setdefault(fontsize, 0)
            accumulator[fontsize] += 1

    # if accumulator is a list, return the entire list
    elif isinstance(accumulator, List):
        accumulator = fontsizes
    
    # if accumulator is a set, add fontsizes to set
    elif isinstance(accumulator, Set):
        for fontsize in fontsizes:
            accumulator.add(fontsize)

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
    fontweights = [
        fontname.split('-')[1]
            if '-' in fontname
            else 'Regular'
        for fontname in fontnames
    ]
    
    # if accumulator is a dictionary, count the fontweights
    if isinstance(accumulator, Dict):
        for fontweight in fontweights:
            accumulator.setdefault(fontweight, 0)
            accumulator[fontweight] += 1

    # if accumulator is a list, return the entire list
    elif isinstance(accumulator, List):
        accumulator = fontweights
    
    # if accumulator is a set, add fontweights to set
    elif isinstance(accumulator, Set):
        for fontweight in fontweights:
            accumulator.add(fontweight)

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
    typefaces = [
        fontname.split('-')[0]
            if '-' in fontname
            else fontname
        for fontname in fontnames
    ]

    # if accumulator is a dictionary, count the typefaces
    if isinstance(accumulator, Dict):
        for typeface in typefaces:
            accumulator.setdefault(typeface, 0)
            accumulator[typeface] += 1

    # if accumulator is a list, return the entire list
    elif isinstance(accumulator, List):
        accumulator = typefaces
    
    # if accumulator is a set, add typefaces to set
    elif isinstance(accumulator, Set):
        for typeface in typefaces:
            accumulator.add(typeface)

    return accumulator

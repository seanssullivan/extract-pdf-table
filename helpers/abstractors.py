# helpers/abstractors.py

# Standard Imports
from collections.abc import Iterator
from typing import Generator, List

# Third-Party Imports
from pdfminer.layout import LTChar


def simplify(characters: Iterator) -> list:
    """Simplify the representation of characters."""
    if isinstance(characters, Generator):
        # Convert generator to list
        characters = list(characters)

    if all(map(lambda char: isinstance(char, LTChar), characters)):
        return simplify_pdfminer_characters(characters)
    else:
        raise NotImplementedError


def simplify_pdfminer_characters(characters: List[LTChar]) -> list:
    """Convert pdfminer.six LTChar objects to dictionaries."""
    return list(map(lambda char: {
        'text': char.get_text(),
        'bbox': {
            'top': char.y1,
            'right': char.x1,
            'bottom': char.y0,
            'left': char.x0,
        },
        'size': char.size,
        'x': char.matrix[4],
        'y': char.matrix[5],
        'font': char.fontname,
        'adv': char.adv
    }, characters))

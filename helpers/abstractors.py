# helpers/abstractors.py

# Standard Imports
from collections.abc import Iterable, Iterator
from typing import Dict, Generator, List

# Third-Party Imports
from pdfminer.layout import LTChar


def simplify(characters: Iterator) -> List:
    """Simplify the representation of characters."""
    if isinstance(characters, Generator):
        # Convert generator to list
        characters = list(characters)

    if all(map(lambda char: isinstance(char, LTChar), characters)):
        return simplify_pdfminer_characters(characters)
    else:
        raise ValueError


def simplify_pdfminer_characters(characters: List[LTChar]) -> List:
    """Convert pdfminer.six LTChar objects to dictionaries."""
    return list(map(lambda char: {
        'text': char.get_text(),
        'top': char.y1,
        'right': char.x1,
        'bottom': char.y0,
        'left': char.x0,
        'size': char.size,
        'x': char.matrix[4],
        'y': char.matrix[5],
        'font': char.fontname,
        'adv': char.adv
    }, characters))


def isolate_table(text: Iterable) -> List:
    line_nums = sorted(map(lambda c: c['line_num'], text))

    # Remove title and any blank lines
    lines = {num: summarize(list(filter(lambda c: c['line_num'] == num, text))) for num in line_nums}
    table_cells = list(filter(lambda c: lines[c['line_num']]['count'] > 1 and lines[c['line_num']]['text'] != '', text))
    return table_cells


def summarize(cells: Iterable) -> Dict:
    if isinstance(cells, Generator):
        # Convert generator to list
        cells = list(cells)

    if all(map(lambda cell: isinstance(cell, LTChar), cells)):
        cells = simplify(cells)

    return {
        'count': len(cells),
        'text': ''.join(list(map(lambda c: c['text'].strip(), cells)))
    }

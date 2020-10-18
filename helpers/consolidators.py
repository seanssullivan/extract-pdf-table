# helpers/consolidators.py

# Standard Imports
from collections.abc import Iterable
from copy import deepcopy
from typing import Dict, List, Literal

# Local Imports
from helpers.comparators import within_margin


def merge_by_proximity(characters: Iterable, margin: int = 0, axis: Literal[0, 1] = 1) -> list:
    """Merge adjacent characters into cells."""

    def merge_characters_within_margin(characters: List[Dict], margin: int = 0, axis: Literal[0, 1] = 1):
        """Combine characters into cells by proximity."""
        characters = sorted(characters, key=lambda obj: obj['left'] if axis == 1 else obj['top'])

        result = []
        cell = characters.pop(0)
        while len(characters) > 0:
            char = characters.pop(0)
            if axis == 0 and within_margin(cell['bottom'], char['top'], margin):
                cell = merge_characters(cell, char, '\n')
            elif axis == 1 and within_margin(cell['right'], char['left'], margin):
                cell = merge_characters(cell, char)
            else:
                result.append(cell)
                cell = char
        else:
            result.append(cell)
        
        return result

    def merge_characters(first: dict, second: dict, separator: str = '') -> dict:
        """Merge two dictionaries representing characters or cells."""
        cell = {
            # Combine both text values
            'text': separator.join([first['text'], second['text']]),

            # Expand bounding box
            'top': min(first['top'], second['top']),
            'bottom': max(first['bottom'], second['bottom']),
            'left': first['left'],
            'right': second['right'],

            # Take lowest line number
            'line_num': min(first['line_num'], second['line_num']),
        }
        return cell

    # Ensure we are not mutating the original list
    characters = deepcopy(characters)

    # Ensure characters are assigned line numbers when merging along x axis
    if not all(map(lambda char: 'line_num' in char, characters)):
        raise ValueError

    if axis == 0:
        raise NotImplementedError
    elif axis == 1:
        # Group characters by line
        num_lines = max(map(lambda obj: obj['line_num'], characters)) + 1
        groups = [list(filter(lambda obj: obj['line_num'] == i, characters)) for i in range(num_lines)]
    else:
        raise ValueError("axis can only be 0 or 1")
    
    cells = []
    for group in groups:
        merged_chars = merge_characters_within_margin(group, margin, axis)
        cells.extend(merged_chars)
    return cells

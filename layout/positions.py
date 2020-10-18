# layout/positions.py

# Standard Imports
from collections.abc import Iterable
from copy import deepcopy
from typing import Generator

# Third-Party Imports
from pdfminer.layout import LTChar


def determine_line_positions(characters: Iterable) -> list:
    """Calculate the positions of lines of text along the vertical axis."""
    if isinstance(characters, Generator):
        # Convert generator to list
        characters = list(characters)

    # Sanity check
    if not all(map(lambda char: 'y' in char, characters)):
        raise ValueError

    if all(map(lambda char: isinstance(char, LTChar), characters)):
        line_positions = sorted(set(map(lambda char: char.matrix[5], characters)), reverse=True)
    elif all(map(lambda char: isinstance(char, dict), characters)):
        line_positions = sorted(set(map(lambda char: char['y'], characters)), reverse=True)
    else:
        raise TypeError

    return line_positions


def assign_characters_to_lines(characters: Iterable, line_positions: list = None) -> list:
    """Assign each character to a line based on its position along the vertical axis."""
    if isinstance(characters, Generator):
        # Convert generator to list
        characters = list(characters)
    else:
        # Ensure we are not mutating the original list
        characters = deepcopy(characters)
    
    # Sanity check
    if not all(map(lambda char: 'y' in char, characters)):
        raise ValueError

    # Calculate line positions if they have not been provided
    if not line_positions:
        line_positions = determine_line_positions(characters)

    if all(map(lambda char: isinstance(char, dict), characters)):
        for character in characters:
            character['line_num'] = line_positions.index(character['y'])
    else:
        raise TypeError
    
    return characters


def determine_column_positions(cells: Iterable) -> list:
    """Calculate column positions along the horizontal axis."""
    if isinstance(cells, Generator):
        # Convert generator to list
        cells = list(cells)

    for cell in cells:
        print(cell)
    
    if all(map(lambda cell: isinstance(cell, dict), cells)):
        pass
    else:
        raise TypeError

    return []
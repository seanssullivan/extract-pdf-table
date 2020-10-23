# layout/positions.py

# Standard Imports
from collections.abc import Iterable
from copy import deepcopy
from typing import Generator, Literal

# Third-Party Imports
from pdfminer.layout import LTChar

# Local Imports
from helpers.abstractors import isolate_table


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


def determine_column_positions(text: Iterable) -> list:
    """Calculate column positions along the horizontal axis."""

    if isinstance(text, Generator):
        # Convert generator to list
        text = list(text)

    if all(map(lambda block: isinstance(block, dict), text)):
        table = isolate_table(text)

        column_positions = []
        for cell in table:
            current = {'left': cell['left'], 'right': cell['right']}
            for other in table:
                if detect_overlap(current, other, axis=1):
                    current['left'] = min(current['left'], other['left'])
                    current['right'] = max(current['right'], other['right'])
            
            column_positions.append((current['left'], current['right']))

    else:
        raise TypeError

    return sorted(set(column_positions))


def detect_overlap(first: dict, second: dict, axis: Literal[0, 1] = 1):
    """Determine if two cells overlap on a given axis."""
    if axis == 0 and first['bottom'] < second['top']:
        return False
    if axis == 0 and first['top'] > second['bottom']:
        return False
    if axis == 1 and first['right'] < second['left']:
        return False
    if axis == 1 and first['left'] > second['right']:
        return False
    return True


def assign_text_to_columns(text: Iterable, column_positions: list = None) -> list:
    """Assign each cell to a column based on its position along the horizontal axis."""
    if isinstance(text, Generator):
        # Convert generator to list
        text = list(text)
    else:
        # Ensure we are not mutating the original list
        text = deepcopy(text)

    # Remove any headers or blank lines
    text = isolate_table(text)

    # Calculate column positions if they have not been provided
    if not column_positions:
        column_positions = determine_column_positions(text)

    if all(map(lambda char: isinstance(char, dict), text)):
        for block in text:
            for position in column_positions:
                coords = {'left': position[0], 'right': position[1]}
                if detect_overlap(block, coords):
                    block['col_num'] = column_positions.index(position)
                    break
        
        assert all(list(map(lambda c: 'col_num' in c, text)))

    else:
        raise TypeError

    return text
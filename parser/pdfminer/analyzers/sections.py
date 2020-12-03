# parser/pdfminer/analyzers/sections.py

# Standard Imports
from typing import Callable, List, Tuple

# Third-Party Imports
from pdfminer.layout import LTItem, LTTextContainer, LTTextLine

# Local Imports
from .. import callbacks as cb
from ..abstractors.position import get_position
from .distribution import determine_distribution
from .divisions import determine_column_positions, determine_row_positions
from ..selectors import select_lines
from ..utils import (
    merge_positions,
    merge_overlapping_positions,
    most_common_fontname,
    most_common_fontsize
)


def determine_header_positions(*items: LTItem, boundaries: Tuple = None) -> Tuple:
    """Determine the position of the table header using the provided elements."""
    header_positions = set()
    header_positions.update(_headers_from_dimensions(*items, boundaries=boundaries))
    header_positions.update(_headers_from_relative_position(*items, boundaries=boundaries))
    header_positions.update(_headers_from_typography(*items, boundaries=boundaries))

    # Iterate over header positions and merge any that overlap
    unique_headers = merge_overlapping_positions(*header_positions)

    if determine_distribution(unique_headers) == 'horizontal':
        # Before returning header, merge into a single position
        merged_header = merge_positions(*unique_headers)
        return [merged_header]

    else:
        # Before returning header positions, sort them from top to bottom
        sorted_positions = sorted(unique_headers, key=lambda col: col[3])
        return sorted_positions


# TODO: Complete function to determine the position of a table footer
def determine_footer_position(*elements: LTItem, boundaries: Tuple = None) -> Tuple:
    pass


# TODO: Complete function to determine the position of a table title
def determine_title_position(*elements: LTItem, boundaries: Tuple = None) -> Tuple:
    pass


def _headers_from_dimensions(*items : LTItem, boundaries: Tuple = None) -> List:
    """Determine the positions of headers from the dimensions of text.
    
    This function is designed to help determine the positions of
    headers and should not be imported into other modules."""
    line_positions = [
        get_position(line)
        for line in _dimensionally_differentiated_text(items, cb.within(boundaries), cb.text.not_blank())
    ]
    header_positions = merge_overlapping_positions(*line_positions)
    return header_positions


def _headers_from_typography(*items : LTItem, boundaries: Tuple = None) -> List:
    """Determine the positions of headers from the font styles of text.
    
    This function is designed to help determine the positions of
    headers and should not be imported into other modules."""
    line_positions = [
        get_position(line)
        for line in _stylistically_differentiated_text(items, cb.within(boundaries), cb.text.not_blank())
    ]
    header_positions = merge_overlapping_positions(*line_positions)
    return header_positions


def _headers_from_relative_position(*items : LTItem, boundaries: Tuple = None) -> List:
    """Determine the positions of headers from the relative position of text.
    
    This function is designed to help determine the positions of
    headers and should not be imported into other modules."""
    line_positions = [
        get_position(
            _positionally_differentiated_text(items, cb.between(column, axis=1))
        ) for column in determine_column_positions(*items, boundaries=boundaries)
    ]
    header_positions = merge_overlapping_positions(*line_positions)
    return header_positions


def _dimensionally_differentiated_text(container: LTTextContainer, *callbacks: Callable) -> List:
    """Determine the positions of text items which differ in fontsize from the average.
    
    This function is designed to help determine the positions of
    headers and should not be imported into other modules."""
    # Retrieve the most common fontsize used throughout the container.
    most_common_size = most_common_fontsize(container)
    
    # Check the font of each textline for differences
    divergent_lines = []
    textlines = select_lines(container, *callbacks)
    for line in textlines:
        line_size = most_common_fontsize(line)
        if line_size != most_common_size:
            divergent_lines.append(line)
    
    return divergent_lines


def _positionally_differentiated_text(container: LTTextContainer, *callbacks: Callable) -> List:
    """Determine the positions of text items which hold a more prominent position.
    
    This function is designed to help determine the positions of
    headers and should not be imported into other modules."""
    # Check the position of each textline for differences
    textlines = select_lines(container, *callbacks)
    return max(textlines, key=lambda ln: ln.y1)


def _stylistically_differentiated_text(container: LTTextContainer, *callbacks: Callable) -> List:
    """Determine the positions of text items which differ in style from the average.

    This function is designed to help determine the positions of
    headers and should not be imported into other modules."""
    # Retrieve the most common font used throughout the container.
    most_common_font = most_common_fontname(container)
    
    # Check the font of each textline for differences
    divergent_lines = []
    textlines = select_lines(container, *callbacks)
    for line in textlines:
        line_font = most_common_fontname(line)
        if line_font != most_common_font:
            divergent_lines.append(line)
    
    return divergent_lines

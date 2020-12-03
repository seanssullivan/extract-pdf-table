# parser/pdfminer/analyzers/divisions.py

# Standard Imports
import itertools
import math
import statistics
from typing import Callable, Iterable, List, Tuple, Union

# Third-Party Imports
from pdfminer.layout import LTContainer, LTItem, LTPage, LTRect, LTTextBox, LTTextLine

# Local Imports
from parser.pdfminer import callbacks as cb
from parser.pdfminer.abstractors import get_position
from parser.pdfminer.utils import merge_overlapping_positions
from parser.pdfminer.selectors import select_lines, select_rectangles, select_textboxes


def determine_column_positions(*items: Union[LTItem, Tuple], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns using the provided layout items."""

    # If argument is an LTPage, use its child containers
    if len(items) == 1 and isinstance(items[0], LTPage):
        items = list(items[0])

    column_positions = []
    # If positions are provided as tuples, extract the left and right sides of each
    if all(map(lambda i: isinstance(i, Tuple), items)):
        columns = _columns_from_bounding_boxes(*items, boundaries=boundaries)
        column_positions.extend(columns)
    
    # If items are instances of LTItems, calculate column positions
    elif all(map(lambda i: isinstance(i, LTItem), items)):
        columns = _columns_from_layout(*items, boundaries=boundaries)
        column_positions.extend(columns)
    
    else:  # Invalid argument type
        args_type = statistics.mode(map(lambda i: type(i), items))
        raise ValueError(f"{args_type!s} is not a valid argument type")

    # Iterate over column positions and remove any overlapping columns
    unique_columns = merge_overlapping_positions(*column_positions)

    # Before returning column positions, sort them from left to right
    sorted_col_positions = sorted(unique_columns, key=lambda col: col[0])
    return sorted_col_positions


def determine_row_positions(*items: Union[LTContainer, Tuple], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows using the provided layout items."""
    
    # If argument is an LTPage, use its child containers
    if len(items) == 1 and isinstance(items[0], LTPage):
        items = list(items[0])

    row_positions = []
    # If positions are provided as tuples, extract the top and bottom of each
    if all(map(lambda i: isinstance(i, Tuple), items)):
        rows = _rows_from_bounding_boxes(*items, boundaries=boundaries)
        row_positions.extend(rows)

     # If items are instances of LTItems, calculate row positions
    elif all(map(lambda i: isinstance(i, LTItem), items)):
        rows = _rows_from_layout(*items, boundaries=boundaries)
        row_positions.extend(rows)

    else:  # Invalid argument type
        args_type = statistics.mode(map(lambda e: type(e), items))
        raise ValueError(f"{args_type!s} is not a valid argument type")

    # Iterate over line positions and remove any overlapping rows
    unique_rows = merge_overlapping_positions(*row_positions)
    
    # Before returning row positions, sort them from top to bottom
    sorted_positions = sorted(unique_rows, key=lambda col: col[0], reverse=True)
    return sorted_positions


def _columns_from_bounding_boxes(*positions: Tuple, boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns from bounding boxes.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    column_positions = [
        _convert_to_column(pos)
        for pos in positions 
        if cb.within(boundaries)(pos)
    ]
    return column_positions


def _rows_from_bounding_boxes(*positions: Tuple, boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows from bounding boxes.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    row_positions = [
        _convert_to_row(pos)
        for pos in positions
        if cb.within(boundaries)(pos)
    ]
    return row_positions


def _columns_from_layout(*items : LTItem, boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns from LTItems.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    column_positions = set()
    # If columns have borders the page will contain LTRect objects
    # Even partial borders will allow us to determine column positions
    if rectangles := select_rectangles(items, cb.within(boundaries)):
        columns = _columns_from_rectangles(*rectangles)
        column_positions.update(columns)
        
    # Otherwise, we'll need to rely on textboxes to estimate column positions
    # Without borders, these dimensions may not account for padding
    if textboxes := select_textboxes(items, cb.within(boundaries), cb.text.not_blank()):
        columns = _columns_from_textboxes(*textboxes)
        column_positions.update(columns)
    
    # Iterate over positions and remove overlapping columns
    columns = merge_overlapping_positions(*column_positions)
    return columns


def _rows_from_layout(*items: LTItem, boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows from LTItems.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    row_positions = set()
    # If rows have borders the page will contain LTRect objects
    # However, we can't determine row positions with only partial borders
    # if rectangles := select_rectangles(items, cb.within(boundaries)):
    #     rows = _rows_from_rectangles(*rectangles)
    #     row_positions.extend(rows)

    # Otherwise, we'll need to rely on lines to estimate row positions
    # Without borders, these dimensions may not account for padding
    if lines := select_lines(items, cb.within(boundaries), cb.text.not_blank()):
        rows = _rows_from_lines(*lines)
        row_positions.update(rows)
    
    # Iterate over positions and remove overlapping rows
    rows = merge_overlapping_positions(*row_positions)
    return rows


def _columns_from_rectangles(*rectangles: LTRect) -> List[Tuple]:
    """Determine the positions of columns from LTRect objects.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    rectangle_positions = _rectangle_positions(rectangles, lambda elem: elem.width > 1)
    column_positions = list(map(lambda pos: _convert_to_column(pos), rectangle_positions))

    # Iterate over positions and remove overlapping columns
    columns = merge_overlapping_positions(*column_positions)
    return columns if len(columns) > 1 else []


def _rows_from_rectangles(*rectangles: LTRect) -> List[Tuple]:
    """Determine the positions of rows from LTRect objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    rectangle_positions = _rectangle_positions(rectangles, lambda elem: elem.height > 1)
    row_positions = list(map(lambda pos: _convert_to_row(pos), rectangle_positions))

    # Iterate over positions and remove overlapping rows
    rows = merge_overlapping_positions(*row_positions)
    return rows if len(rows) > 1 else []


def _columns_from_textboxes(*textboxes: LTTextBox) -> List[Tuple]:
    """Determine the positions of columns from LTTextBox objects.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    textbox_positions = _textbox_positions(textboxes)
    column_positions = list(map(lambda pos: _convert_to_column(pos), textbox_positions))
    
    # Iterate over positions and remove overlapping columns
    columns = merge_overlapping_positions(*column_positions)
    return columns if len(columns) > 1 else []


def _rows_from_textboxes(*textboxes: LTTextBox) -> List:
    """Determine the positions of rows from LTTextBox objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    textbox_positions = _textbox_positions(textboxes)
    row_positions = list(map(lambda pos: _convert_to_row(pos), textbox_positions))
    
    # Iterate over positions and remove overlapping rows
    rows = merge_overlapping_positions(*row_positions)
    return rows if len(rows) > 1 else []


def _columns_from_lines(*lines: LTTextLine) -> List[Tuple]:
    """Determine the positions of columns from LTTextLine objects.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    line_positions = _line_positions(lines)
    column_positions = list(map(lambda pos: _convert_to_column(pos), line_positions))
    
    # Iterate over positions and remove overlapping columns
    columns = merge_overlapping_positions(*column_positions)
    return columns if len(columns) > 1 else []


def _rows_from_lines(*lines: LTTextLine) -> List[Tuple]:
    """Determine the positions of rows from LTTextLine objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    line_positions = _line_positions(lines, lambda elem: elem.height > 1)
    row_positions = list(map(lambda pos: _convert_to_row(pos), line_positions))
    
    # Iterate over positions and remove overlapping rows
    rows = merge_overlapping_positions(*row_positions)
    return rows if len(rows) > 1 else []


def _rectangle_positions(rectangles: Iterable[LTRect], *callbacks: Callable) -> List[Tuple]:
    """Determine the positions of LTRect objects.
    
    This function is designed to help determine the positions of
    columns and rows and should not be imported into other modules."""
    
    # Extract the positions of rectangles
    rectangle_positions = [
        get_position(rectangle)
        for rectangle in rectangles
        if isinstance(rectangle, LTRect)
        and all(map(lambda cb: cb(rectangle), callbacks))
    ]
    return rectangle_positions


def _textbox_positions(textboxes: Iterable[LTTextBox], *callbacks) -> List[Tuple]:
    """Determine the positions of LTTextBox objects.
    
    This function is designed to help determine the positions of
    columns and rows and should not be imported into other modules."""

    # Extract the positions of textboxes
    textbox_positions = [
        get_position(textbox)
        for textbox in textboxes
        if isinstance(textbox, LTTextBox)
        and all(map(lambda cb: cb(textbox), callbacks))
    ]
    return textbox_positions


def _line_positions(lines: Iterable[LTTextLine], *callbacks) -> List[Tuple]:
    """Determine the positions of rows using LTTextLine objects.
    
    This function is designed to help determine the positions of
    columns and rows and should not be imported into other modules."""

    # Determine positions of rows
    line_positions = [
        get_position(line)
        for line in lines
        if isinstance(line, LTTextLine)
        and all(map(lambda cb: cb(line), callbacks))
    ]
    return line_positions


def _convert_to_column(position: Tuple) -> Tuple:
    """Convert a bounding box to column position.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    return (position[0], position[2])


def _convert_to_row(position: Tuple) -> Tuple:
    """Convert a bounding box to row position.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    return (position[1], position[3])


# def _calculate_column_positions_using_quantiles(positions) -> List:
#     """Calculate the positions of columns using quantiles."""

#     def max_iterations(positions):
#         dimensions = list(zip(*positions))
#         max_width = max(dimensions[2]) - min(dimensions[0])
#         avg_width = statistics.mean(dimensions[2]) - statistics.mean(dimensions[0])
#         iterations = math.floor(max_width / avg_width)
#         return iterations

#     def intersect(positions, cut_points):
#         for position, point in itertools.product(positions, cut_points):
#             if (position[0] < point) and (position[2] > point):
#                 return True
        
#         return False

#     log.info("Calculating column positions using quantiles...")

#     # Set max number of iterations
#     iterations = max_iterations(positions)

#     edges = list(itertools.chain.from_iterable(positions))
#     print(edges)

#     columns = {}
#     for div in range(2, iterations):
#         cut_points = statistics.quantiles(edges, n=div)
#         if not intersect(positions, cut_points):
#             columns[div] = cut_points

#     return columns

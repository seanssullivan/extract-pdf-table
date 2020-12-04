# parser/pdfminer/analyzers/divisions.py

# Standard Imports
import itertools
import math
from operator import itemgetter
import statistics
from typing import List, Tuple, Union

# Third-Party Imports
from pdfminer.layout import LTContainer, LTItem, LTPage, LTRect, LTTextBox, LTTextLine

# Local Imports
from .. import callbacks as cb
from ..reducers import reduce_positions
from ..utils import estimate_bounding_box, merge_overlapping_positions
from ..selectors import (
    select_lines,
    select_rectangles,
    select_textboxes
)


def determine_column_positions(*items: Union[LTItem, Tuple], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns using the provided layout items."""

    # If argument is an LTPage, use its child containers
    if len(items) == 1 and isinstance(items[0], LTPage):
        items = list(items[0])

    column_positions = []
    # If items are instances of LTItems, calculate column positions
    if all(map(lambda i: isinstance(i, LTItem), items)):
        columns = _columns_from_layout(*items, boundaries=boundaries)
        column_positions.extend(columns)
    
    # If positions are provided as tuples, extract the left and right sides of each
    elif all(map(lambda i: isinstance(i, Tuple), items)):
        columns = [itemgetter(0, 2)(pos) for pos in items if cb.within(boundaries)(pos)]
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

     # If items are instances of LTItems, calculate row positions
    if all(map(lambda i: isinstance(i, LTItem), items)):
        rows = _rows_from_layout(*items, boundaries=boundaries)
        row_positions.extend(rows)
    
    elif all(map(lambda i: isinstance(i, Tuple), items)):
        rows = [itemgetter(1, 3)(pos) for pos in items if cb.within(boundaries)(pos)]
        row_positions.extend(rows)

    else:  # Invalid argument type
        args_type = statistics.mode(map(lambda e: type(e), items))
        raise ValueError(f"{args_type!s} is not a valid argument type")

    # Iterate over line positions and remove any overlapping rows
    unique_rows = merge_overlapping_positions(*row_positions)
    
    # Before returning row positions, sort them from top to bottom
    sorted_positions = sorted(unique_rows, key=lambda col: col[0], reverse=True)
    return sorted_positions


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
    unique_columns = merge_overlapping_positions(*column_positions)
    # return unique_columns

    # Expand columns to fit margins and padding
    margins = itemgetter(0, 2)(estimate_bounding_box(*items))
    columns = _fit_columns_to_margins(margins, unique_columns)
    # columns = _fit_columns_to_padding(columns)
    return columns


def _rows_from_layout(*items: LTItem, boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows from LTItems.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    row_positions = set()
    # If rows have borders the page will contain LTRect objects
    # However, we can't determine row positions with only partial borders
    if rectangles := select_rectangles(items, cb.within(boundaries)):
        rows = _rows_from_rectangles(*rectangles)
        row_positions.update(rows)

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
    rectangle_positions = reduce_positions([], rectangles, lambda elem: elem.height > 1 and elem.width < 1)
    horizontal_positions = set(map(lambda pos: itemgetter(0, 2)(pos), rectangle_positions))

    # Iterate over positions and remove overlapping columns.
    unique_positions = merge_overlapping_positions(*horizontal_positions)

    # Sort positions from left to right
    sorted_positions = sorted(unique_positions, key=lambda col: col[0])

    # Pair positions into tuples representing the left and right sides of columns
    columns = _pair_positions(list(itertools.chain.from_iterable(sorted_positions))[1:-1], 2)

    # Return columns if more than one
    return columns if len(columns) > 1 else []


def _rows_from_rectangles(*rectangles: LTRect) -> List[Tuple]:
    """Determine the positions of rows from LTRect objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    rectangle_positions = reduce_positions([], rectangles, lambda elem: elem.width > 1 and elem.height < 1)
    row_positions = set(map(lambda pos: itemgetter(1, 3)(pos), rectangle_positions))

    # Iterate over positions and remove overlapping rows
    unique_positions = merge_overlapping_positions(*row_positions)

    # Sort positions from top to bottom
    sorted_positions = sorted(unique_positions, key=lambda row: row[0])

    # Pair positions into tuples representing the bottom and top of row
    rows = _pair_positions(list(itertools.chain.from_iterable(sorted_positions))[1:-1], 2)

    # Return rows if more than one
    return rows if len(rows) > 1 else []


def _columns_from_textboxes(*textboxes: LTTextBox) -> List[Tuple]:
    """Determine the positions of columns from LTTextBox objects.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    textbox_positions = reduce_positions([], textboxes)
    column_positions = list(map(lambda pos: itemgetter(0, 2)(pos), textbox_positions))
    
    # Iterate over positions and remove overlapping columns
    columns = merge_overlapping_positions(*column_positions)
    return columns if len(columns) > 1 else []


def _rows_from_textboxes(*textboxes: LTTextBox) -> List:
    """Determine the positions of rows from LTTextBox objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    textbox_positions = reduce_positions([], textboxes)
    row_positions = list(map(lambda pos: itemgetter(1, 3)(pos), textbox_positions))
    
    # Iterate over positions and remove overlapping rows
    rows = merge_overlapping_positions(*row_positions)
    return rows if len(rows) > 1 else []


def _columns_from_lines(*lines: LTTextLine) -> List[Tuple]:
    """Determine the positions of columns from LTTextLine objects.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    line_positions = reduce_positions([], lines)
    column_positions = list(map(lambda pos: itemgetter(0, 2)(pos), line_positions))
    
    # Iterate over positions and remove overlapping columns
    columns = merge_overlapping_positions(*column_positions)
    return columns if len(columns) > 1 else []


def _rows_from_lines(*lines: LTTextLine) -> List[Tuple]:
    """Determine the positions of rows from LTTextLine objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    line_positions = reduce_positions([], lines, lambda elem: elem.height > 1)
    row_positions = list(map(lambda pos: itemgetter(1, 3)(pos), line_positions))
    
    # Iterate over positions and remove overlapping rows
    rows = merge_overlapping_positions(*row_positions)
    return rows if len(rows) > 1 else []


def _fit_columns_to_margins(margins, columns):
    """Expand left and right sides of columns to fit margins."""
    expanded_columns = [
        (margins[0], columns[0][1]),  # Left-most column
        *columns[1:-1],               # Middle columns
        (columns[-1][0], margins[1])  # Right-most column
    ] if len(columns) > 1 else [margins]
    return expanded_columns


def _fit_columns_to_padding(columns):
    """Expand column edges to reflect cell padding."""
    # Find exact position between columns
    column_divisions = []
    for i in range(0, len(columns) - 1):
        position = (columns[i][1] + columns[i+1][0]) / 2
        column_divisions.append(round(position, 3))

    # Update sides of columns to consume padding
    expanded_columns = []
    for idx, col in enumerate(columns):
        left_side = column_divisions[idx - 1] + 0.25 if idx > 0 else col[0]
        right_side = column_divisions[0] - 0.25 if idx < len(columns) - 1 else col[1]
        expanded_columns.append((left_side, right_side))
    
    return expanded_columns


def _pair_positions(iterable, n, fillvalue=None):
    """
    Group positions from a list into pairs.
    
    Based on the 'grouper' recipe from 
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * n
    pairs = itertools.zip_longest(*args, fillvalue=fillvalue)
    return list(pairs)


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

# parser/pdfminer/analyzers/divisions.py

# Standard Imports
import itertools
import math
from operator import itemgetter
import statistics
from typing import Iterable, List, Tuple, Union

# Third-Party Imports
from pdfminer.layout import LTContainer, LTItem, LTPage, LTRect, LTTextBox, LTTextLine

# Local Imports
from .. import callbacks as cb
from .alignment import determine_alignment
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

    # If items are instances of LTItems, calculate column positions
    if all(map(lambda i: isinstance(i, LTItem), items)):
        column_positions = _columns_from_layout(items, boundaries=boundaries)
    
    # If positions are provided as tuples, extract the left and right sides of each
    elif all(map(lambda i: isinstance(i, Tuple), items)):
        column_positions = _columns_from_positions(items, boundaries=boundaries)
    
    else:  # Invalid argument type
        args_type = statistics.mode(map(lambda i: type(i), items))
        raise ValueError(f"{args_type!s} is not a valid argument type")

    # Iterate over column positions and remove any overlapping columns
    unique_column_positions = merge_overlapping_positions(*column_positions)

    # Before returning column positions, sort them from left to right
    sorted_column_positions = sorted(unique_column_positions, key=lambda col: col[0])
    return sorted_column_positions


def determine_row_positions(*items: Union[LTContainer, Tuple], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows using the provided layout items."""
    # If argument is an LTPage, use its child containers
    if len(items) == 1 and isinstance(items[0], LTPage):
        items = list(items[0])

    # If items are instances of LTItems, calculate row positions
    if all(map(lambda i: isinstance(i, LTItem), items)):
        row_positions = _rows_from_layout(items, boundaries=boundaries)
    
    # If positions are provided as tuples, extract the top and bottom of each
    elif all(map(lambda i: isinstance(i, Tuple), items)):
        row_positions = _rows_from_positions(items, boundaries=boundaries)

    else:  # Invalid argument type
        args_type = statistics.mode(map(lambda e: type(e), items))
        raise ValueError(f"{args_type!s} is not a valid argument type")

    # Iterate over line positions and remove any overlapping rows
    unique_row_positions = merge_overlapping_positions(*row_positions)
    
    # Before returning row positions, sort them from top to bottom
    sorted_row_positions = sorted(unique_row_positions, key=lambda col: col[0], reverse=True)
    return sorted_row_positions


def _columns_from_layout(items: Iterable[LTItem], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns from LTItems.

    Columns are discovered by analyzing LTItems in order of decreasing primacy:
    The boxes formed by LTRect objects sometimes contain multiple textboxes and
    are therefore analyzed first; textboxes nearly always align with columns and
    are therefore analyzed second; while LTTextLine objects typically contain
    data from a single cell and are therefore analyzed last.

    We could determine column positions by only analyzing LTTextLine objects;
    however, empty cells and varying alignments produce unreliable results.
    In addition, by working downwards, we maintain as much of the margins
    and padding as possible.
    
    This function was designed to help determine the positions of
    columns and should not be imported into other modules."""
    column_positions = set()
    # If columns have borders the page will contain LTRect objects
    # Even partial borders will allow us to determine column positions
    if rectangles := select_rectangles(items, cb.within(boundaries), lambda r: r.height > 1 and r.width < 1):
        positions = _column_positions_from_rectangles(rectangles)
        _update_positions(column_positions, positions)
        
    # Otherwise, we'll need to rely on textboxes to estimate column positions
    # Without borders, these dimensions may not account for padding
    if textboxes := select_textboxes(items, cb.within(boundaries), cb.text.not_blank()):
        positions = _column_positions_from_textboxes(textboxes)
        _update_positions(column_positions, positions)

    # As a last resort, we'll also use textlines to estimate column positions
    # Without borders or textboxes, these dimensions may not account for padding
    if textlines := select_lines(items, cb.within(boundaries), cb.text.not_blank()):
        positions = _column_positions_from_textlines(textlines)
        _update_positions(column_positions, positions)

    # Iterate over positions and remove overlapping columns
    unique_positions = merge_overlapping_positions(*column_positions)

    # Sort positions from left to right
    sorted_positions = sorted(unique_positions, key=lambda col: col[0])

    # Expand columns to better fit margins and padding
    margins = itemgetter(0, 2)(estimate_bounding_box(*items))
    positions = _fit_columns_to_margins(sorted_positions, margins)
    positions = _adjust_column_padding_based_on_alignment(positions, items)
    return positions


def _rows_from_layout(items: Iterable[LTItem], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows from LTItems.

    Rows are discovered by analyzing LTItems in order of decreasing primacy:
    textboxes often exceed the vertical boundaries set by LTRect objects and
    are therefore analyzed first; LTRect objects can surround multiple lines
    and are therefore analyzed second; while LTTextLine objects typically
    contain data from a single cell and are therefore analyzed last.

    We could determine row positions by only analyzing LTTextLine objects;
    however, empty cells and varying alignments produce unreliable results.
    In addition, by working downwards, we maintain as much of the margins
    and padding as possible.
    
    This function was designed to help determine the positions of
    rows and should not be imported into other modules."""
    row_positions = set()
    # Begin by using textboxes to narrow-down row positions
    # These dimensions typically exceed the actual size of rows
    if textboxes := select_textboxes(items, cb.within(boundaries), cb.text.not_blank()):
        positions = _row_positions_from_textboxes(textboxes)
        _update_positions(row_positions, positions)

    # If rows have borders the page will contain LTRect objects
    # However, we won't determine row positions with only partial borders
    if rectangles := select_rectangles(items, cb.within(boundaries), lambda r: r.width > 1 and r.height < 1):
        positions = _row_positions_from_rectangles(rectangles)
        _update_positions(row_positions, positions)

    # Otherwise, we'll need to rely on textlines to estimate row positions
    # Without borders, these dimensions may not account for padding
    if textlines := select_lines(items, cb.within(boundaries), cb.text.not_blank(), lambda l: l.height > 1):
        positions = _row_positions_from_textlines(textlines)
        _update_positions(row_positions, positions)

    # Iterate over positions and remove overlapping rows
    unique_positions = merge_overlapping_positions(*row_positions)

    # Sort positions from top to bottom
    sorted_positions = sorted(unique_positions, key=lambda row: row[0], reverse=True)
    assert all(map(lambda pos: isinstance(pos, tuple), sorted_positions))

    # Expand rows to better fit padding
    positions = _adjust_row_padding_based_on_alignment(sorted_positions, items)
    return positions


def _column_positions_from_rectangles(rectangles: Iterable[LTRect], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns from LTRect objects.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    rectangle_positions = reduce_positions([], rectangles)
    horizontal_positions = [itemgetter(0, 2)(pos) for pos in rectangle_positions if cb.within(boundaries)(pos)]

    # Iterate over positions and remove overlapping columns.
    unique_positions = merge_overlapping_positions(*horizontal_positions)

    # Sort positions from left to right
    sorted_positions = sorted(unique_positions, key=lambda col: col[0])

    # Pair positions into tuples representing the left and right sides of each column
    column_positions = _pair_positions(list(itertools.chain.from_iterable(sorted_positions))[1:-1], 2)

    return column_positions


def _row_positions_from_rectangles(rectangles: Iterable[LTRect], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows from LTRect objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    rectangle_positions = reduce_positions([], rectangles)
    vertical_positions = [itemgetter(1, 3)(pos) for pos in rectangle_positions if cb.within(boundaries)(pos)]

    # Iterate over positions and remove overlapping rows
    unique_positions = merge_overlapping_positions(*vertical_positions)

    # Sort positions from top to bottom
    sorted_positions = sorted(unique_positions, key=lambda row: row[0])

    # Pair positions into tuples representing the bottom and top of row
    row_positions = _pair_positions(list(itertools.chain.from_iterable(sorted_positions))[1:-1], 2)

    return row_positions


def _column_positions_from_textboxes(textboxes: Iterable[LTTextBox], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns from LTTextBox objects.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    textbox_positions = reduce_positions([], textboxes)
    horizontal_positions = [itemgetter(0, 2)(pos) for pos in textbox_positions if cb.within(boundaries)(pos)]
    
    # Iterate over positions and remove overlapping columns
    unique_positions = merge_overlapping_positions(*horizontal_positions)

    # Sort positions from left to right
    sorted_positions = sorted(unique_positions, key=lambda col: col[0])

    return sorted_positions


def _row_positions_from_textboxes(textboxes: Iterable[LTTextBox], boundaries: Tuple = None) -> List:
    """Determine the positions of rows from LTTextBox objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    textbox_positions = reduce_positions([], textboxes)
    vertical_positions = [itemgetter(1, 3)(pos) for pos in textbox_positions if cb.within(boundaries)(pos)]
    
    # Iterate over positions and remove overlapping rows
    unique_positions = merge_overlapping_positions(*vertical_positions)

    # Sort positions from top to bottom
    sorted_positions = sorted(unique_positions, key=lambda row: row[0])

    return sorted_positions


def _column_positions_from_textlines(lines: Iterable[LTTextLine], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns from LTTextLine objects.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    textline_positions = reduce_positions([], lines)
    horizontal_positions = [itemgetter(0, 2)(pos) for pos in textline_positions if cb.within(boundaries)(pos)]
    
    # Iterate over positions and remove overlapping columns
    unique_positions = merge_overlapping_positions(*horizontal_positions)

    # Sort positions from left to right
    sorted_positions = sorted(unique_positions, key=lambda col: col[0])

    return sorted_positions


def _row_positions_from_textlines(lines: Iterable[LTTextLine], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows from LTTextLine objects.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    textline_positions = reduce_positions([], lines)
    vertical_positions = [itemgetter(1, 3)(pos) for pos in textline_positions if cb.within(boundaries)(pos)]
    
    # Iterate over positions and remove overlapping rows
    unique_positions = merge_overlapping_positions(*vertical_positions)

    # Sort positions from top to bottom
    sorted_positions = sorted(unique_positions, key=lambda row: row[0])

    return sorted_positions


def _columns_from_positions(positions: Iterable[Tuple], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of columns from tuples of item positions.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    horizontal_positions = [itemgetter(0, 2)(pos) for pos in positions if cb.within(boundaries)(pos)]

    # Iterate over positions and remove overlapping columns
    unique_positions = merge_overlapping_positions(*horizontal_positions)

    # Sort positions from left to right
    sorted_positions = sorted(unique_positions, key=lambda col: col[0])

    return sorted_positions


def _rows_from_positions(positions: Iterable[Tuple], boundaries: Tuple = None) -> List[Tuple]:
    """Determine the positions of rows from tuples of item positions.
    
    This function is designed to help determine the positions of
    rows and should not be imported into other modules."""
    vertical_positions = [itemgetter(1, 3)(pos) for pos in positions if cb.within(boundaries)(pos)]
    
    # Iterate over positions and remove overlapping rows
    unique_positions = merge_overlapping_positions(*vertical_positions)

    # Sort positions from top to bottom
    sorted_positions = sorted(unique_positions, key=lambda row: row[0])

    return sorted_positions


def _update_positions(found: set, new: list) -> set:
    """Update set of positions after checking whether any will be overwritten.
    
    This function is designed to help determine the positions of
    columns and should not be imported into other modules."""
    children = lambda pos: list(filter(cb.between(pos, axis=0), new))
    remove = [position for position in found if len(children(position)) > 1]
    found.difference_update(set(remove))
    found.update(new)


def _fit_columns_to_margins(columns, margins):
    """Expand left and right sides of columns to fit margins."""
    expanded_columns = [
        (margins[0], columns[0][1]),  # Left-most column
        *columns[1:-1],               # Middle columns
        (columns[-1][0], margins[1])  # Right-most column
    ] if len(columns) > 1 else [margins]
    return expanded_columns


def _adjust_column_padding_based_on_alignment(columns, items):
    """Expand column edges to reflect cell padding."""
    alignments = []
    for column in columns:
        textlines = select_lines(items, cb.between(column), cb.text.not_blank())
        alignments.append(determine_alignment(*textlines))

    expanded_columns = []
    for idx, col in enumerate(columns):
        # Calculate left side position
        if alignments[idx] == 'left' or idx == 0:
            left_side = col[0]
        else:
            left_side = columns[idx - 1][0] + 0.5 \
                if alignments[idx - 1] == 'right' \
                    else (columns[idx - 1][1] + col[0]) / 2

        # Calculate right side position
        if alignments[idx] == 'right' or idx == len(columns) - 1:
            right_side = col[1]
        else:
            right_side = columns[idx + 1][0] - 0.5 \
                if alignments[idx + 1] == 'left' \
                    else (col[1] + columns[idx + 1][0]) / 2

        position = (left_side, right_side)
        expanded_columns.append(position)
    
    return expanded_columns


def _adjust_row_padding_based_on_alignment(rows, items):
    """Expand row edges to reflect cell padding."""
    alignments = []
    for row in rows:
        textlines = select_lines(items, cb.between(row, axis=0), cb.text.not_blank())
        alignments.append(determine_alignment(*textlines))

    expanded_rows = []
    for idx, row in enumerate(rows):
        # Calculate top position
        if alignments[idx] == 'top' or idx == 0:
            top = row[1]
        else:
            top = rows[idx - 1][0] - 0.5 \
                if alignments[idx - 1] == 'bottom' \
                    else (row[1] + rows[idx - 1][0]) / 2

        # Calculate bottom position
        if alignments[idx] == 'bottom' or idx == len(rows) - 1:
            bottom = row[0]
        else:
            bottom = rows[idx + 1][1] + 0.5 \
                if alignments[idx + 1] == 'top' \
                    else (rows[idx + 1][1] + row[0]) / 2

        position = (bottom, top)
        expanded_rows.append(position)
    
    return expanded_rows


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

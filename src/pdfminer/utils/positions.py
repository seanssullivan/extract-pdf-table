# parser/pdfminer/utils/positions.py

# Standard Imports
from functools import reduce
from typing import List, Tuple

# Third-Party Imports
from pdfminer.layout import LTItem

# Local Imports
from ..abstractors import get_position


def estimate_bounding_box(*items: LTItem) -> Tuple:
    """Estimate the position of a bounding box which encloses all provided layout items."""
    item_positions = [get_position(item)for item in items]
    bbox = merge_positions(*item_positions)
    return bbox


def merge_positions(*positions):
    """Merge multiple positions."""
    position = list(zip(*positions))

    if len(position) == 2:
        return (min(position[0]),  # left or bottom
                max(position[1]))  # right or top
    elif len(position) == 4:
        return (min(position[0]),  # left
                min(position[1]),  # bottom
                max(position[2]),  # right
                max(position[3]))  # top
    else:
        raise ValueError(f"cannot merge positions with {len(position)} dimensions")


def merge_overlapping_positions(*positions: Tuple) -> List:
    """Merge overlapping positions and return any that are distinct."""
    result = reduce(_merge_on_overlap, positions, []) if len(positions) > 0 else []
    return result


def _merge_on_overlap(accumulator: List, position: Tuple) -> List:
    """Merge overlapping positions.
    
    This function is designed to help merge positions
    and should not be imported into other modules."""

    # Sanity check
    if len(position) != 2 and len(position) != 4:
        raise ValueError(f"cannot merge positions with {len(position)} dimensions")

    unique_positions = []
    for pos in accumulator:
        if len(position) == 2 and \
            (position[0] > pos[1] or position[1] < pos[0]):    # positions do not overlap
            unique_positions.append(pos)                       # therefore position is unique

        elif len(position) == 4 and \
            (position[0] > pos[2] or position[2] < pos[0]      # positions do not overlap horizontally
            or position[1] > pos[3] or position[3] < pos[0]):  # positions do not overlap vertically
            unique_positions.append(pos)                       # therefore position is unique

        else:                                                  # positions overlap
            position = merge_positions(position, pos)          # therefore merge them

    # Return all unique positions
    return sorted(
        [position] + unique_positions,
        key=lambda pos: (pos[0], pos[-1])
    )

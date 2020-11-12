# parser/pdfminer/analyzers/distribution.py

# Standard Imports
from typing import Text, Tuple, Union

# Third-Party Imports
from pdfminer.layout import LTContainer


def distributed_horizontally(*elements: Union[LTContainer, Tuple]) -> bool:
    """Return whether the positions provided are distributed horizontally."""

    # If only one element is provided, apply function to its children
    if len(elements) == 1 and isinstance(elements[0], LTContainer):
        return distributed_horizontally(*list(elements[0]))

    # Convert any LTContainers to tuples of their positions
    if all(map(lambda el: isinstance(el, LTContainer), elements)):
        elements = map(lambda e: (e.x0, e.y0, e.x1, e.y1), elements)

    for index, current in enumerate(elements):
        for neighbor in elements[index + 1:]:
            # Return false if any position is entirely above or below others
            if current[1] >= neighbor[3] or current[3] <= neighbor[1]:
                return False
            
            # Calculate horizontal and vertical overlap
            horizontal_overlap = _calculate_horizontal_overlap(current, neighbor)
            vertical_overlap = _calculate_vertical_overlap(current, neighbor)
            
            # Use overlap to determine whether alignment is more horizontal or more vertical
            if horizontal_overlap > vertical_overlap:
                return False

    # For all other cases, return True
    return True


def distributed_vertically(*elements: Union[LTContainer, Tuple]) -> bool:
    """Return whether the positions provided are distributed vertically."""

    # If only one element is provided, apply function to its children
    if len(elements) == 1 and isinstance(elements[0], LTContainer):
        return distributed_vertically(*list(elements[0]))

    # Convert any LTContainers to tuples of their positions
    if all(map(lambda el: isinstance(el, LTContainer), elements)):
        elements = map(lambda e: (e.x0, e.y0, e.x1, e.y1), elements)

    for index, current in enumerate(elements):
        for neighbor in elements[index + 1:]:
            # Return false if any position is entirely left or right of others
            if current[0] >= neighbor[2] or current[2] <= neighbor[0]:
                return False
            
            # Calculate horizontal and vertical overlap
            horizontal_overlap = _calculate_horizontal_overlap(current, neighbor)
            vertical_overlap = _calculate_vertical_overlap(current, neighbor)
            
            # Use overlap to determine whether alignment is more horizontal or more vertical
            if vertical_overlap > horizontal_overlap:
                return False

    # For all other cases, return True
    return True


def _calculate_horizontal_overlap(first: Tuple, second: Tuple) -> float:
    """Calculate horizontal overlap of two bounding boxes."""
    # If first overlaps second on the left
    if first[0] <= second[0] and first[2] > second[0]:
        horizontal_overlap = first[2] - second[0]

    # Else if first overlaps second on the right
    elif first[2] >= second[2] and first[0] < second[2]:
        horizontal_overlap = second[2] - first[0]

    else:  # no overlap exists
        horizontal_overlap = 0

    # Return overlap distance
    return horizontal_overlap


def _calculate_vertical_overlap(first: Tuple, second: Tuple) -> float:
    """Calculate vertical overlap of two bounding boxes."""
    # If first overlaps second on the top
    if first[1] <= second[1] and first[3] > second[1]:
        vertical_overlap = first[3] - second[1]

    # Else if first overlaps second on the bottom
    elif first[3] >= second[3] and first[1] < second[3]:
        vertical_overlap = second[3] - first[1]

    else:  # no overlap exists
        vertical_overlap = 0

    # Return overlap distance
    return vertical_overlap

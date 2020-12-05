# parser/pdfminer/analyzers/distribution.py

# Standard Imports
from typing import Text, Tuple, Union

# Third-Party Imports
from pdfminer.layout import LTContainer


def determine_distribution(*positions: Union[LTContainer, Tuple]) -> Text:
    """Return whether the positions provided are distributed horizontally or vertically."""

    # If only one element is provided, apply function to its children
    if len(positions) == 1 and isinstance(positions[0], LTContainer):
        return determine_distribution(*list(positions[0]))

    # Convert any LTContainers to tuples of their positions
    if all(map(lambda pos: isinstance(pos, LTContainer), positions)):
        positions = list(map(lambda p: (p.x0, p.y0, p.x1, p.y1), positions))

    overlaps = []
    for index, current in enumerate(positions):
        for neighbor in positions[index + 1:]:
            # Calculate horizontal and vertical overlap
            overlaps.append((
                _calculate_vertical_overlap(current, neighbor),
                _calculate_horizontal_overlap(current, neighbor)
            ))
            
    # Use overlaps to determine whether alignment is more horizontal or more vertical
    if all(map(lambda o: o[0] > o[1], overlaps)):
        return 'horizontal'
    elif all(map(lambda o: o[0] < o[1], overlaps)):
        return 'vertical'
    else:
        return None


def _calculate_horizontal_overlap(first: Tuple, second: Tuple) -> float:
    """Calculate horizontal overlap of two bounding boxes."""
    # if first overlaps second on the left
    if first[0] <= second[0] and first[2] > second[0] and first[2] <= second[2]:
        horizontal_overlap = first[2] - second[0]

    # else if first overlaps second on the right
    elif first[0] >= second[0] and first[0] < second[2] and first[2] >= second[2]:
        horizontal_overlap = second[2] - first[0]
    
    # else if first entirely inside second
    elif first[0] >= second[0] and first[2] <= second[2]:
        horizontal_overlap = first[2] - first[0]
    
    # else if second entirely inside first
    elif first[0] <= second[0] and first[2] >= second[2]:
        horizontal_overlap = second[2] - second[0]

    else:  # no overlap exists
        horizontal_overlap = 0

    # return overlap distance
    return horizontal_overlap


def _calculate_vertical_overlap(first: Tuple, second: Tuple) -> float:
    """Calculate vertical overlap of two bounding boxes."""
    # if first overlaps second on the top
    if first[1] <= second[1] and first[3] > second[1] and first[3] <= second[3]:
        vertical_overlap = first[3] - second[1]

    # else if first overlaps second on the bottom
    elif first[1] >= second[1] and first[1] < second[3] and first[3] >= second[3]:
        vertical_overlap = second[3] - first[1]

    # else if first entirely inside second
    elif first[1] >= second[1] and first[3] <= second[3]:
        vertical_overlap = first[3] - first[1]
    
    # else if second entirely inside first
    elif first[1] <= second[1] and first[3] >= second[3]:
        vertical_overlap = second[3] - second[1]

    else:  # no overlap exists
        vertical_overlap = 0

    # return overlap distance
    return vertical_overlap

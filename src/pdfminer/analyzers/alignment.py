# src/pdfminer/analyzers/alignment.py

# Standard Imports
import statistics
from typing import Text, Tuple, Union

# Third-Party Imports
from pdfminer.layout import LTItem, LTAnno

# Local Imports
from .distribution import determine_distribution


def determine_alignment(*positions: Union[LTItem, Tuple]) -> Text:
    """Return the direction in which the positions are aligned."""

    # If only one element is provided, apply function to its children
    if len(positions) == 1 and isinstance(positions[0], LTItem):
        return determine_alignment(*list(positions[0]))

    # Convert any LTItem to tuples of their positions
    if all(map(lambda pos: isinstance(pos, LTItem), positions)):
        positions = [(p.x0, p.y0, p.x1, p.y1) for p in positions if not isinstance(p, LTAnno)]

    distribution = determine_distribution(*positions)
    # Calculate standard deviations
    if distribution == 'horizontal':
        stdev = {
            'top': _calculate_stdev("top", *positions),
            'middle': _calculate_stdev("middle", *positions),
            'bottom': _calculate_stdev("bottom", *positions)
        }
    elif distribution == 'vertical':
        stdev = {
            'left': _calculate_stdev("left", *positions),
            'center': _calculate_stdev("center", *positions),
            'right': _calculate_stdev("right", *positions)
        }
    else:
        return None

    return min(stdev, key=stdev.get)


def _calculate_stdev(alignment, *positions: Union[Tuple]) -> float:
    """Calculate the standard deviation.

    This function is designed to help determine alignment and
    should not be imported into other modules."""

    calculations = {
        'left': lambda pos: pos[0],
        'bottom': lambda pos: pos[1],
        'right': lambda pos: pos[2],
        'top': lambda pos: pos[3],
        'center': lambda pos: (pos[0] + pos[2]) / 2,
        'middle': lambda pos: (pos[1] + pos[3]) / 2,
    }

    # Calculate the standard deviation
    dimensions = map(calculations[alignment], positions)
    standard_deviation = statistics.stdev(dimensions)
    return standard_deviation

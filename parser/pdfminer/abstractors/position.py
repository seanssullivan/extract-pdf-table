# parser/pdfminer/abstractors/position.py

# Standard Imports
from typing import Tuple

# Third-Party Imports
from pdfminer.layout import LTItem


def get_position(item: LTItem) -> Tuple:
    """Extract position from an LTItem."""
    return (round(item.x0, 3),  # left
            round(item.y0, 3),  # bottom
            round(item.x1, 3),  # right
            round(item.y1, 3))  # top

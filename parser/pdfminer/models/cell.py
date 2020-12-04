# parser/pdfminer/models/cell.py

# Standard Imports
from typing import List

# Third-Party Imports
from pdfminer.layout import LTChar, LTContainer, LTTextLineHorizontal


class LTCell(LTContainer):

    def __init__(self, bbox):
        LTContainer.__init__(self, bbox)

    def add(self, element) -> None:
        if isinstance(element, LTTextLineHorizontal):
            super().extend(list(element))
        elif isinstance(element, LTChar):
            super().add(element)
        else:
            raise ValueError

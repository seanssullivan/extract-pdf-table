# parser/pdfminer/models/cell.py

# Standard Imports
from typing import List

# Third-Party Imports
from pdfminer.layout import LTChar, LTContainer, LTTextLineHorizontal


class LTCell(LTContainer):

    def __init__(self, bbox):
        LTContainer.__init__(self, bbox)
        self.column = None
        self.row = None

    @property
    def column(self):
        return self.__col_index

    @column.setter
    def column(self, value):
        self.__col_index = value

    @property
    def row(self):
        return self.__row_index

    @row.setter
    def row(self, value):
        self.__row_index = value

    def add(self, element) -> None:
        if isinstance(element, LTTextLineHorizontal):
            super().extend(list(element))
        elif isinstance(element, LTChar):
            super().add(element)
        else:
            raise ValueError

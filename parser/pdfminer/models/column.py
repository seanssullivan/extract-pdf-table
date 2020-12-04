# parser/pdfminer/models/column.py

# Third-Party Imports
from pdfminer.layout import LTContainer

# Local Imports
from .cell import LTCell


class LTColumn(LTContainer):

    def __init__(self, bbox):
        LTContainer.__init__(self, bbox)
        self.cells = []

    def __iter__(self):
        return iter(self._objs)

    def __len__(self):
        return len(self._objs)

    def add(self, cell) -> None:
        if isinstance(cell, LTCell):
            self.cells.append(cell)
        else:
            raise ValueError

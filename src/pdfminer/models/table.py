# src/pdfminer/models/table.py

# Standard Imports
from typing import List

# Third-Party Imports
import pandas as pd
from pdfminer.layout import LTComponent, LTPage

# Local Imports
from .cell import LTCell
from .column import LTColumn
from .row import LTRow


class LTTable(LTComponent):

    def __init__(self, bbox):
        # Determine bounding box
        # x0, y0, x1, y1 = zip(*map(lambda c: (c.x0, c.y0, c.x1, c.y1), cells))
        # bbox = (min(x0), min(y0), max(x1), max(y1))
        LTComponent.__init__(self, bbox)
        self.cells = []
        self.columns = []
        self.rows = []

    @classmethod
    def from_page(cls, page: LTPage):
        raise NotImplementedError

    @classmethod
    def from_cells(cls, cells: List):
        raise NotImplementedError

    @classmethod
    def from_columns(cls, columns: List):
        raise NotImplementedError

    @classmethod
    def from_rows(cls, rows: List):
        raise NotImplementedError

    def __iter__(self):
        return iter(self._objs)

    def __len__(self):
        return len(self._objs)

    def add(self, element) -> None:
        if isinstance(element, LTCell):
            self.cells.append(element)
        elif isinstance(element, LTColumn):
            self.columns.append(element)
        elif isinstance(element, LTRow):
            self.rows.append(element)
        else:
            raise ValueError("must be an instance of LTCell, LTColumn, or LTRow")

    def extend(self, elements) -> None:
        for element in elements:
            self.add(element)

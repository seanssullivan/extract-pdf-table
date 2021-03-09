# src/parser/models/column.py

# Standard Imports
from typing import List

# Local Imports
from .cell import Cell
from .container import Container


class Column(Container):

    def __init__(self, cells: List):
        Container.__init__(self, cells)

    @property
    def cells(self):
        return self.children

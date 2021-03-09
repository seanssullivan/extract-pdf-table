# src/parser/models/cell.py

# Standard Imports
from typing import List

# Local Imports
from .container import Container


class Cell(Container):

    def __init__(self, contents: List):
        Container.__init__(self, contents)
        self.column = None
        self.row = None

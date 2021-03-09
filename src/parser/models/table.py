# src/parser/models/table.py

# Standard Imports
from typing import List

# Third-Party Imports
import pandas as pd

# Local Imports
from .column import Column
from .container import Container
from .row import Row


class Table(Container):

    def __init__(self, contents):
        Container.__init__(self, contents)

    def add(self, element) -> None:
        if isinstance(element, Column):
            self.columns.append(element)
        elif isinstance(element, Row):
            self.rows.append(element)
        else:
            raise ValueError("must be an instance of Column, or Row")

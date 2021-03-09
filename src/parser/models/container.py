# src/parser/models/container.py

# Standard Imports
from typing import List

# Local Imports
from .component import Component


class Container(Component):

    def __init__(self, elements: List):
        Component.__init__(self, self.determine_bounding_box(elements))
        self.children = elements if elements else []

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    def add(self, element) -> None:
        if isinstance(element, Component):
            self.children.append(element)
        else:
            raise TypeError

    def extend(self, elements: List) -> None:
        for element in elements:
            self.add(element)

    @staticmethod
    def determine_bounding_box(elements: List):
        """Determine bounding box from child elements."""
        x0, y0, x1, y1 = zip(*map(lambda e: e.bbox, elements))
        bbox = (min(x0), min(y0), max(x1), max(y1))
        return bbox

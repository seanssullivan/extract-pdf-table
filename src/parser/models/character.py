# src/parser/models/character.py

# Local Imports
from .component import Component


class Character(Component):

    def __init__(self, text: str, bbox: tuple):
        Component.__init__(self, bbox)
        self.text = text

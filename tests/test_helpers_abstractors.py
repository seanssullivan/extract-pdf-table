# tests/test_helpers_abstractors.py

# Standard Imports
from typing import Dict, List
import unittest

# Third-Party Imports
from pdfminer.layout import LTChar

# Local Imports
from helpers.abstractors import simplify
from helpers.extractors import extract_pages, extract_characters


class TestSimplify(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_2.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))
    
    def test_returns_list(self) -> None:
        result = simplify(extract_characters(self.test_pages[0]))
        self.assertIsInstance(result, List)

    def test_pdfminer_characters_returns_list_containing_dictionaries(self) -> None:
        characters = simplify(extract_characters(self.test_pages[0]))
        for char in characters:
            self.assertIsInstance(char, Dict)
    
    def test_list_does_not_contain_pdfminer_chars(self) -> None:
        characters = simplify(extract_characters(self.test_pages[0]))
        for char in characters:
            self.assertNotIsInstance(char, LTChar)

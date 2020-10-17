# Standard Imports
import unittest

# Third-Party Imports
from pdfminer.layout import LTChar

# Local Imports
from helpers.abstractors import simplify
from helpers.selectors import extract_pages, extract_characters


class TestSimplify(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_2.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))
    
    def test_returns_list(self) -> None:
        result = simplify(extract_characters(self.test_pages[0]))
        self.assertIsInstance(result, list)

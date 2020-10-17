# Standard Imports
import unittest

# Third-Party Imports
import pandas as pd

# Local Imports
from extract_table import extract_table
from helpers.selectors import extract_pages


class TestTableExtraction(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_3.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))

    def test_returns_dataframe(self) -> None:
        result = extract_table(self.test_pages[0])
        self.assertIsInstance(result, pd.DataFrame)

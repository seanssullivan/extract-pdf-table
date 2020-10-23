# tests/test_table_extraction.py

# Standard Imports
import unittest

# Third-Party Imports
import pandas as pd
from pandas._testing import assert_frame_equal

# Local Imports
from extract_table import extract_table
from helpers.extractors import extract_pages


class TestTableExtraction(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_3.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))

    def test_returns_dataframe(self) -> None:
        result = extract_table(self.test_pages[0])
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_returns_table_data(self) -> None:
        result = extract_table(self.test_pages[0])
        expected = pd.DataFrame([
            {'IdField': '1', 'NameField': 'Name1', 'TestField1': 'Value1', 'TestField2': 'Value1', 'TestField3': 'Value1'},
            {'IdField': '2', 'NameField': 'Name2', 'TestField1': 'Value2', 'TestField2': 'Value2', 'TestField3': 'Value2'},
            {'IdField': '3', 'NameField': 'Name3', 'TestField1': 'Value3', 'TestField2': 'Value3', 'TestField3': 'Value3'},
            {'IdField': '4', 'NameField': 'Name4', 'TestField1': 'Value4', 'TestField2': 'Value4', 'TestField3': 'Value4'},
        ])
        assert_frame_equal(result, expected)

    def test_returns_none_when_no_text_found(self) -> None:
        result = extract_table([])
        self.assertIsNone(result)

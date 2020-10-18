# tests/test_helpers_consolidators.py

# Standard Imports
import unittest

# Local Imports
from helpers.consolidators import merge_by_proximity
from helpers.extractors import extract_pages, extract_characters


class TestMergeByProximity(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_3.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))

    def test_returns_list(self):
        example = [
            {'text': '', 'top': 0, 'right': 10, 'bottom': 10, 'left': 0, 'line_num': 0},
        ]
        result = merge_by_proximity(example)
        self.assertIsInstance(result, list)

    def test_merges_characters_horizontally(self):
        example = [
            {'text': 't', 'top': 0, 'left': 0, 'right': 10, 'bottom': 10, 'line_num': 0},
            {'text': 'e', 'top': 0, 'left': 10, 'right': 20, 'bottom': 10, 'line_num': 0},
            {'text': 's', 'top': 0, 'left': 20, 'right': 30, 'bottom': 10, 'line_num': 0},
            {'text': 't', 'top': 0, 'left': 30, 'right': 40, 'bottom': 10, 'line_num': 0},
        ]
        result = merge_by_proximity(example)

        expected = [{'text': 'test', 'top': 0, 'right': 40, 'bottom': 10, 'left': 0, 'line_num': 0}]
        self.assertListEqual(result, expected)

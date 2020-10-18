# tests/test_layout_positions.py

# Standard Imports
import unittest

# Local Imports
from helpers.abstractors import simplify
from helpers.extractors import extract_pages, extract_characters
from layout.positions import determine_line_positions, determine_column_positions, assign_characters_to_lines


class TestDetermineLinePositions(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_3.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))
    
    def test_returns_list(self) -> None:
        characters = simplify(extract_characters(self.test_pages[0]))
        result = determine_line_positions(characters)
        self.assertIsInstance(result, list)

    def test_returns_line_positions(self) -> None:
        characters = simplify(extract_characters(self.test_pages[0]))
        result = determine_line_positions(characters)
        expected = [709.47, 693.22, 679.47, 665.45, 651.45, 637.7, 623.7]
        self.assertListEqual(result, expected)


class TestAssignCharactersToLines(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_3.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))
    
    def test_returns_list(self) -> None:
        characters = simplify(extract_characters(self.test_pages[1]))
        result = assign_characters_to_lines(characters)
        self.assertIsInstance(result, list)

    def test_assigns_line_numbers(self) -> None:
        characters = simplify(extract_characters(self.test_pages[1]))
        assigned_chars = assign_characters_to_lines(characters)

        for char in assigned_chars:
            self.assertIn('line_num', char)

    def test_does_not_mutate_original(self) -> None:
        characters = simplify(extract_characters(self.test_pages[1]))
        assigned_chars = assign_characters_to_lines(characters)
        self.assertNotEqual(characters, assigned_chars)

        for char in characters:
            self.assertNotIn('line_num', char)
    
    def test_assigns_correct_lines(self) -> None:
        characters = simplify(extract_characters(self.test_pages[1]))
        line_positions = determine_line_positions(characters)
        assigned_chars = assign_characters_to_lines(characters)

        for char in assigned_chars:
            self.assertEqual(char['line_num'], line_positions.index(char['y']))


class TestDetermineColumnPositions(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_3.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))
    
    def test_returns_list(self) -> None:
        characters = simplify(extract_characters(self.test_pages[0]))
        result = determine_column_positions(characters)
        self.assertIsInstance(result, list)


class TestAssignCharactersToColumns(unittest.TestCase):
    pass
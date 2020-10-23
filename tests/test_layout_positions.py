# tests/test_layout_positions.py

# Standard Imports
from statistics import mean
import unittest

# Local Imports
from helpers.abstractors import simplify
from helpers.consolidators import merge_by_proximity
from helpers.extractors import extract_pages, extract_characters
from layout.positions import determine_line_positions, determine_column_positions, assign_characters_to_lines, assign_text_to_columns


class TestDetermineLinePositions(unittest.TestCase):

    def setUp(self) -> None:
        with open('tests/samples/sample_3.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))
    
    def test_returns_list_of_floats(self) -> None:
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
        with open('tests/samples/sample_4.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))
    
    def test_returns_list(self) -> None:
        example = [
            {'text': 'Test', 'top': 0, 'left': 0, 'right': 10, 'bottom': 10, 'line_num': 0}
        ]
        result = determine_column_positions(example)
        self.assertIsInstance(result, list)

    def test_returns_column_positions(self) -> None:
        example = [
            {'text': 'TestField1', 'top': 0, 'left': 0, 'right': 100, 'bottom': 10, 'line_num': 0},
            {'text': 'TestValue1', 'top': 15, 'left': 0, 'right': 100, 'bottom': 25, 'line_num': 1},
            {'text': 'TestField2', 'top': 0, 'left': 200, 'right': 300, 'bottom': 10, 'line_num': 0},
            {'text': 'TestValue2', 'top': 15, 'left': 200, 'right': 300, 'bottom': 25, 'line_num': 1},
            {'text': 'TestField2', 'top': 0, 'left': 400, 'right': 500, 'bottom': 10, 'line_num': 0},
            {'text': 'TestValue2', 'top': 15, 'left': 400, 'right': 500, 'bottom': 25, 'line_num': 1},
        ]
        result = determine_column_positions(example)
        expected = [(0, 100), (200, 300), (400, 500)]
        self.assertListEqual(result, expected)


class TestAssignCharactersToColumns(unittest.TestCase):
    
    def setUp(self) -> None:
        with open('tests/samples/sample_3.pdf', 'rb') as test_file:
            self.test_pages = list(extract_pages(test_file))

    def test_returns_list(self) -> None:
        characters = simplify(extract_characters(self.test_pages[1]))
        margin = mean(map(lambda char: char['size'], characters))
        lines = assign_characters_to_lines(characters)
        blocks = merge_by_proximity(lines, margin, axis=1)
        result = assign_text_to_columns(blocks)
        self.assertIsInstance(result, list)

    def test_assigns_line_numbers(self) -> None:
        characters = simplify(extract_characters(self.test_pages[1]))
        margin = mean(map(lambda char: char['size'], characters))
        lines = assign_characters_to_lines(characters)
        blocks = merge_by_proximity(lines, margin, axis=1)
        result = assign_text_to_columns(blocks)

        for block in result:
            self.assertIn('col_num', block)

    def test_does_not_mutate_original(self) -> None:
        characters = simplify(extract_characters(self.test_pages[1]))
        margin = mean(map(lambda char: char['size'], characters))
        lines = assign_characters_to_lines(characters)
        blocks = merge_by_proximity(lines, margin, axis=1)
        result = assign_text_to_columns(blocks)
        self.assertNotEqual(blocks, result)

        for block in blocks:
            self.assertNotIn('col_num', block)

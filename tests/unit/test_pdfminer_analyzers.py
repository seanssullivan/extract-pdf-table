# tests/unit/test_pdfminer_analyzers.py

# Standard Imports
import unittest

# Local Imports
from parser.pdfminer.analyzers.alignment import determine_alignment
from parser.pdfminer.analyzers.distribution import determine_distribution



class TestDetermineAlignment(unittest.TestCase):

    def test_returns_string_value(self) -> None:
        test_positions = [(0, 0, 10, 10), (0, 10, 10, 20)]
        result = determine_alignment(*test_positions)
        self.assertIsInstance(result, str)
    
    def test_returns_left_when_left_aligned(self) -> None:
        test_positions = [(0, 40, 10, 50), (0, 30, 6, 40), (0, 20, 30, 30), (0, 10, 20, 20), (0, 0, 14, 10)]
        result = determine_alignment(*test_positions)
        self.assertEqual(result, 'left')

    def test_returns_center_when_center_aligned(self) -> None:
        test_positions = [(10, 40, 20, 50), (12, 30, 18, 40), (0, 20, 30, 30), (5, 10, 25, 20), (8, 0, 22, 10)]
        result = determine_alignment(*test_positions)
        self.assertEqual(result, 'center')
    
    def test_returns_right_when_right_aligned(self) -> None:
        test_positions = [(40, 40, 50, 50), (44, 30, 50, 40), (20, 20, 50, 30), (30, 10, 50, 20), (36, 0, 50, 10)]
        result = determine_alignment(*test_positions)
        self.assertEqual(result, 'right')

    def test_returns_top_when_top_aligned(self) -> None:
        test_positions = [(40, 40, 50, 50), (30, 44, 40, 50), (20, 20, 30, 50), (10, 30, 20, 50), (0, 36, 10, 50)]
        result = determine_alignment(*test_positions)
        self.assertEqual(result, 'top')

    def test_returns_middle_when_middle_aligned(self) -> None:
        test_positions = [(40, 10, 50, 20), (30, 12, 40, 18), (20, 0, 30, 30), (10, 5, 20, 25), (0, 8, 10, 22)]
        result = determine_alignment(*test_positions)
        self.assertEqual(result, 'middle')
    
    def test_returns_bottom_when_bottom_aligned(self) -> None:
        test_positions = [(0, 0, 10, 14), (10, 0, 20, 20), (20, 0, 30, 30), (30, 0, 40, 6), (40, 0, 50, 10)]
        result = determine_alignment(*test_positions)
        self.assertEqual(result, 'bottom')


class TestDetermineDistribution(unittest.TestCase):

    def test_returns_string_value_when_positions_aligned(self) -> None:
        test_positions = [(0, 0, 10, 10), (0, 10, 10, 20)]
        result = determine_distribution(*test_positions)
        self.assertIsInstance(result, str)
    
    def test_returns_horizontal_when_positions_aligned_vertically(self) -> None:
        test_positions = [(0, 0, 10, 10), (10, 0, 20, 10)]
        result = determine_distribution(*test_positions)
        self.assertEqual(result, 'horizontal')

    def test_returns_vertical_when_positions_aligned_horizontally(self) -> None:
        test_positions = [(0, 0, 10, 10), (0, 10, 10, 20)]
        result = determine_distribution(*test_positions)
        self.assertEqual(result, 'vertical')

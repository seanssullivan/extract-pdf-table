# tests/test_helpers_abstractors.py

# Standard Imports
import unittest

# Local Imports
from helpers.comparators import within_proximity



class TestWithinProximity(unittest.TestCase):

    def test_returns_boolean(self):
        first = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0}
        second = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0}
        result = within_proximity(first, second)
        self.assertIsInstance(result, bool)

    def test_returns_true_when_in_proximity(self):
        first = {'top': 0, 'right': 10, 'bottom': 10, 'left': 0}
        second = {'top': 10, 'right': 12, 'bottom': 20, 'left': 2}
        result = within_proximity(first, second)
        self.assertTrue(result)

    def test_returns_false_when_not_in_proximity(self):
        first = {'top': 0, 'right': 10, 'bottom': 10, 'left': 0}
        second = {'top': 20, 'right': 30, 'bottom': 30, 'left': 20}
        result = within_proximity(first, second)
        self.assertFalse(result)

    def test_returns_true_when_within_margin(self):
        first = {'top': 0, 'right': 10, 'bottom': 10, 'left': 0}
        second = {'top': 20, 'right': 30, 'bottom': 30, 'left': 20}
        result = within_proximity(first, second, margin=10)
        self.assertTrue(result)

    def test_returns_true_when_in_proximity_on_x_axis(self):
        first = {'top': 0, 'right': 10, 'bottom': 10, 'left': 0}
        second = {'top': 1, 'right': 20, 'bottom': 11, 'left': 10}
        result = within_proximity(first, second, axis=1)
        self.assertTrue(result)
    
    def test_returns_true_when_in_proximity_on_y_axis(self):
        first = {'top': 0, 'right': 10, 'bottom': 10, 'left': 0}
        second = {'top': 10, 'right': 11, 'bottom': 20, 'left': 1}
        result = within_proximity(first, second, axis=0)
        self.assertTrue(result)

    def test_returns_true_when_within_margin_on_x_axis(self):
        first = {'top': 0, 'right': 10, 'bottom': 10, 'left': 0}
        second = {'top': 1, 'right': 24, 'bottom': 11, 'left': 14}
        result = within_proximity(first, second, axis=1, margin=5)
        self.assertTrue(result)
    
    def test_returns_true_when_within_margin_on_y_axis(self):
        first = {'top': 0, 'right': 10, 'bottom': 10, 'left': 0}
        second = {'top': 18, 'right': 11, 'bottom': 28, 'left': 1}
        result = within_proximity(first, second, axis=0, margin=10)
        self.assertTrue(result)

# tests/unit/test_pdfminer_callbacks.py

# Standard Imports
from dataclasses import dataclass
import unittest

# Local Imports
from parser.pdfminer import callbacks


class Container:
    def __init__(self, text: str = ''):
        self._text = text
    
    def get_text(self):
        return self._text


@dataclass(frozen=True)
class LayoutItem:
    x0: int
    y0: int
    x1: int
    y1: int


class TestCallbackBetween(unittest.TestCase):

    def test_returns_boolean(self) -> None:
        test_element = LayoutItem(10, 0, 20, 40)
        callback = callbacks.between()
        result = callback(test_element)
        self.assertIsInstance(result, bool)

    def test_returns_true_for_horizontal_axis(self) -> None:
        test_element = LayoutItem(10, 0, 20, 40)
        test_horizontal = (5, 25)
        callback = callbacks.between(test_horizontal, axis=1)
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_true_for_vertical_axis(self) -> None:
        test_element = LayoutItem(0, 10, 40, 20)
        test_vertical = (5, 25)
        callback = callbacks.between(test_vertical, axis=0)
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_false_if_outside_boundary(self) -> None:
        test_element = LayoutItem(0, 0, 10, 10)
        test_boundary = (15, 25)
        callback = callbacks.between(test_boundary)
        result = callback(test_element)
        self.assertFalse(result)

    def test_returns_true_if_exactly_matches_boundary(self) -> None:
        test_element = LayoutItem(10, 10, 30, 30)
        test_boundary = (10, 30)
        callback = callbacks.between(test_boundary)
        result = callback(test_element)
        self.assertTrue(result)


class TestCallbackWithin(unittest.TestCase):

    def test_returns_boolean(self) -> None:
        test_element = LayoutItem(5, 5, 15, 15)
        callback = callbacks.within()
        result = callback(test_element)
        self.assertIsInstance(result, bool)
    
    def test_returns_true_if_inside_boundary(self) -> None:
        test_element = LayoutItem(5, 5, 15, 15)
        test_boundary = (0, 0, 20, 20)
        callback = callbacks.within(test_boundary)
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_false_if_outside_boundary(self) -> None:
        test_element = LayoutItem(0, 0, 10, 10)
        test_boundary = (15, 15, 25, 25)
        callback = callbacks.within(test_boundary)
        result = callback(test_element)
        self.assertFalse(result)

    def test_returns_true_if_exactly_boundary(self) -> None:
        test_element = LayoutItem(10, 10, 30, 30)
        test_boundary = (10, 10, 30, 30)
        callback = callbacks.within(test_boundary)
        result = callback(test_element)
        self.assertTrue(result)


class TestCallbackTextEquals(unittest.TestCase):
    
    def test_returns_boolean(self) -> None:
        test_element = Container('test')
        callback = callbacks.text.equals('test')
        result = callback(test_element)
        self.assertIsInstance(result, bool)

    def test_returns_true_if_text_equal(self) -> None:
        test_element = Container('test')
        callback = callbacks.text.equals('test')
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_false_if_text_not_equal(self) -> None:
        test_element = Container('text')
        callback = callbacks.text.equals('test')
        result = callback(test_element)
        self.assertFalse(result)
    

class TestCallbackTextDoesNotEqual(unittest.TestCase):
    
    def test_returns_boolean(self) -> None:
        test_element = Container('test')
        callback = callbacks.text.does_not_equal('test')
        result = callback(test_element)
        self.assertIsInstance(result, bool)

    def test_returns_true_if_text_not_equal(self) -> None:
        test_element = Container('text')
        callback = callbacks.text.does_not_equal('test')
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_false_if_text_equal(self) -> None:
        test_element = Container('test')
        callback = callbacks.text.does_not_equal('test')
        result = callback(test_element)
        self.assertFalse(result)
    

class TestCallbackTextIncludes(unittest.TestCase):
    
    def test_returns_boolean(self) -> None:
        test_element = Container('test')
        callback = callbacks.text.includes('test')
        result = callback(test_element)
        self.assertIsInstance(result, bool)

    def test_returns_true_if_text_includes_string(self) -> None:
        test_element = Container('test')
        callback = callbacks.text.includes('s')
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_false_if_text_does_not_include_string(self) -> None:
        test_element = Container('cat')
        callback = callbacks.text.includes('s')
        result = callback(test_element)
        self.assertFalse(result)
    
    def test_returns_true_if_text_includes_all_strings(self) -> None:
        test_element = Container('test')
        callback = callbacks.text.includes('e', 's', 't')
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_false_if_text_does_not_include_all_strings(self) -> None:
        test_element = Container('cat')
        callback = callbacks.text.includes('c', 's', 't')
        result = callback(test_element)
        self.assertFalse(result)


class TestCallbackTextIsBlank(unittest.TestCase):

    def test_returns_true_if_text_is_blank(self) -> None:
        test_element = Container('')
        callback = callbacks.text.is_blank()
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_false_if_text_is_not_blank(self) -> None:
        test_element = Container('cat')
        callback = callbacks.text.is_blank()
        result = callback(test_element)
        self.assertFalse(result)


class TestCallbackTextNotBlank(unittest.TestCase):

    def test_returns_true_if_text_is_not_blank(self) -> None:
        test_element = Container('dog')
        callback = callbacks.text.not_blank()
        result = callback(test_element)
        self.assertTrue(result)

    def test_returns_false_if_text_is_blank(self) -> None:
        test_element = Container('')
        callback = callbacks.text.not_blank()
        result = callback(test_element)
        self.assertFalse(result)

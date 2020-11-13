# tests/unit/test_pdfminer_abstractors.py

# Standard Imports
from dataclasses import dataclass
import unittest

# Local Imports
from parser.pdfminer.abstractors import get_fontname
from parser.pdfminer.abstractors import get_fontsize
from parser.pdfminer.abstractors import get_fontweight
from parser.pdfminer.abstractors import get_typeface
from parser.pdfminer.abstractors import get_position


@dataclass(frozen=True)
class Char:
    fontname: str
    size: int


class TestGetFontname(unittest.TestCase):

    def setUp(self) -> None:
        self.char = Char('BCDEEE+Arial-Bold', 12)

    def test_returns_string(self):
        result = get_fontname(self.char)
        self.assertIsInstance(result, str)
    
    def test_returns_fontname(self):
        result = get_fontname(self.char)
        self.assertEqual(result, 'Arial-Bold')


class TestGetFontsize(unittest.TestCase):

    def setUp(self) -> None:
        self.char = Char('Calibri', 12)

    def test_returns_integer(self):
        result = get_fontsize(self.char)
        self.assertIsInstance(result, int)
    
    def test_returns_fontsize(self):
        result = get_fontsize(self.char)
        self.assertEqual(result, 12)


class TestGetFontweight(unittest.TestCase):

    def setUp(self) -> None:
        self.char = Char('BCDEEE+Arial-Bold', 10)

    def test_returns_string(self):
        result = get_fontweight(self.char)
        self.assertIsInstance(result, str)
    
    def test_returns_fontweight(self):
        result = get_fontweight(self.char)
        self.assertEqual(result, 'Bold')


class TestGetTypeface(unittest.TestCase):

    def setUp(self) -> None:
        self.char = Char('BCDEEE+TimesNewRoman-Italic', 12)

    def test_returns_string(self):
        result = get_typeface(self.char)
        self.assertIsInstance(result, str)
    
    def test_returns_typeface(self):
        result = get_typeface(self.char)
        self.assertEqual(result, 'TimesNewRoman')


@dataclass(frozen=True)
class Bbox:
    x0: int
    y0: int
    x1: int
    y1: int


class TestGetPosition(unittest.TestCase):

    def setUp(self) -> None:
        self.bbox = Bbox(0, 10, 10, 0)

    def test_returns_tuple(self):
        result = get_position(self.bbox)
        self.assertIsInstance(result, tuple)
    
    def test_returns_typeface(self):
        result = get_position(self.bbox)
        self.assertTupleEqual(result, (0, 10, 10, 0))
    
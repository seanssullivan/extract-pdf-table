# tests/unit/test_pdfminer_abstractors.py

# Standard Imports
from dataclasses import dataclass

# Local Imports
from src.parser.abstractors import get_fontname
from src.parser.abstractors import get_fontsize
from src.parser.abstractors import get_fontweight
from src.parser.abstractors import get_typeface
from src.parser.abstractors import get_position


@dataclass(frozen=True)
class Char:
    fontname: str
    size: int


class TestGetFontname():

    def test_returns_string(self):
        char = Char('BCDEEE+Arial-Bold', 12)
        result = get_fontname(char)
        assert isinstance(result, str)

    def test_returns_fontname(self):
        char = Char('BCDEEE+Arial-Bold', 12)
        result = get_fontname(char)
        assert result == 'Arial-Bold'


class TestGetFontsize():

    def setUp(self) -> None:
        self.char = Char('Calibri', 12)

    def test_returns_integer(self):
        char = Char('Calibri', 12)
        result = get_fontsize(char)
        assert isinstance(result, int)

    def test_returns_fontsize(self):
        char = Char('Calibri', 12)
        result = get_fontsize(char)
        assert result == 12


class TestGetFontweight():

    def test_returns_string(self):
        char = Char('BCDEEE+Arial-Bold', 10)
        result = get_fontweight(char)
        assert isinstance(result, str)

    def test_returns_fontweight(self):
        char = Char('BCDEEE+Arial-Bold', 10)
        result = get_fontweight(char)
        assert result == 'Bold'


class TestGetTypeface():

    def setUp(self) -> None:
        self.char = Char('BCDEEE+TimesNewRoman-Italic', 12)

    def test_returns_string(self):
        char = Char('BCDEEE+TimesNewRoman-Italic', 12)
        result = get_typeface(char)
        assert isinstance(result, str)

    def test_returns_typeface(self):
        char = Char('BCDEEE+TimesNewRoman-Italic', 12)
        result = get_typeface(char)
        assert result == 'TimesNewRoman'


@dataclass(frozen=True)
class Bbox:
    x0: int
    y0: int
    x1: int
    y1: int


class TestGetPosition():

    def test_returns_tuple(self):
        bbox = Bbox(0, 10, 10, 0)
        result = get_position(bbox)
        assert isinstance(result, tuple)

    def test_returns_typeface(self):
        bbox = Bbox(0, 10, 10, 0)
        result = get_position(bbox)
        assert result == (0, 10, 10, 0)

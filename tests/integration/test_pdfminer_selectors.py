# tests/integration/test_pdfminer_selectors.py

# Standard Imports
from typing import Iterable

# Third-Party Imports
from pdfminer.layout import LTChar, LTPage, LTRect, LTTextBox, LTTextLine
import pytest

# Local Imports
from parser.pdfminer.selectors import select_pages
from parser.pdfminer.selectors import select_textboxes
from parser.pdfminer.selectors import select_rectangles
from parser.pdfminer.selectors import select_lines
from parser.pdfminer.selectors import select_characters


class TestSelectPages():

    def test_returns_iterable(self, multiple_pages) -> None:
        result = select_pages(multiple_pages)
        assert isinstance(result, Iterable)

    def test_returns_pages(self, multiple_pages) -> None:
        result = select_pages(multiple_pages)
        for page in result:
            assert isinstance(page, LTPage)

    def test_filters_results_with_callback_function(self, multiple_pages) -> None:
        callback = lambda pg: any(map(lambda obj: isinstance(obj, LTTextBox), pg))
        result = list(select_pages(multiple_pages, callback))
        assert len(result) == 3

    def test_filters_results_with_multiple_callbacks(self, multiple_pages) -> None:
        callbacks = [
            lambda pg: any(map(lambda obj: isinstance(obj, LTTextBox), pg)),
            lambda pg: any(map(lambda obj: "3" in obj.get_text(), pg))]
        result = list(select_pages(multiple_pages, *callbacks))
        assert len(result) == 1

    def test_returns_empty_list_when_no_matches_with_callback(self, multiple_pages) -> None:
        result = list(select_pages(multiple_pages, lambda pg: any(map(lambda obj: isinstance(obj, LTRect), pg))))
        assert len(result) == 0


class TestSelectTextboxes():

    @pytest.fixture(autouse=True)
    def text(self, paragraphs):
        return paragraphs[0]

    @pytest.fixture(autouse=True)
    def table(self, table_borders):
        return table_borders[0]

    def test_returns_iterable(self, text) -> None:
        result = select_textboxes(text)
        assert isinstance(result, Iterable)

    def test_returns_textboxes_from_single_page(self, text) -> None:
        result = select_textboxes(text)
        for textbox in result:
            assert isinstance(textbox, LTTextBox)

    def test_returns_textboxes_from_multiple_pages(self, paragraphs) -> None:
        result = select_textboxes(paragraphs)
        for textbox in result:
            assert isinstance(textbox, LTTextBox)

    def test_filters_results_with_callback_function(self, table) -> None:
        result = list(select_textboxes(table, lambda box:  "4" in box.get_text()))
        assert len(result) == 4

    def test_filters_results_with_multiple_callbacks(self, table) -> None:
        callbacks = [lambda box:  "4" in box.get_text(), lambda box: box.x1 < 250]
        result = list(select_textboxes(table, *callbacks))
        assert len(result) == 2

    def test_returns_empty_list_when_no_matches_with_callback(self, table) -> None:
        callbacks = [lambda box:  "Z" in box.get_text()]
        result = list(select_textboxes(table, *callbacks))
        assert len(result) == 0


class TestSelectRectangles():

    @pytest.fixture(autouse=True)
    def table(self, table_borders):
        return table_borders[0]

    def test_returns_iterable(self, table) -> None:
        result = select_rectangles(table)
        assert isinstance(result, Iterable)

    def test_returns_rectangles_from_single_page(self, table) -> None:
        result = select_rectangles(table)
        for rectangle in result:
            assert isinstance(rectangle, LTRect)

    def test_returns_rectangles_from_multiple_pages(self, table_borders) -> None:
        result = select_rectangles(table_borders)
        for rectangle in result:
            assert isinstance(rectangle, LTRect)


class TestSelectLines():

    @pytest.fixture(autouse=True)
    def text(self, paragraphs):
        return paragraphs[0]

    @pytest.fixture(autouse=True)
    def boxes(self, text):
        return list(select_textboxes(text))

    def test_returns_iterable(self, boxes) -> None:
        result = select_lines(boxes[0])
        assert isinstance(result, Iterable)

    def test_returns_lines_from_single_textbox(self, boxes) -> None:
        result = select_lines(boxes[0])
        for line in result:
            assert isinstance(line, LTTextLine)

    def test_returns_lines_from_multiple_textboxes(self, boxes) -> None:
        result = select_lines(boxes)
        for line in result:
            assert isinstance(line, LTTextLine)
    
    def test_returns_lines_from_single_page(self, text) -> None:
        result = select_lines(text)
        for line in result:
            assert isinstance(line, LTTextLine)
    
    def test_returns_lines_from_multiple_pages(self, text) -> None:
        result = select_lines(text)
        for line in result:
            assert isinstance(line, LTTextLine)

    def test_filters_results_with_callback_function(self, text) -> None:
        result = list(select_lines(text, lambda ln:  "v" in ln.get_text()))
        assert len(result) == 3

    def test_filters_results_with_multiple_callbacks(self, text) -> None:
        callbacks = [lambda box:  "v" in box.get_text(), lambda box: box.y0 > 550,  lambda box: box.y1 < 600]
        result = list(select_lines(text, *callbacks))
        assert len(result) == 1
    
    def test_returns_empty_list_when_no_matches_with_callback(self, text) -> None:
        callbacks = [lambda box:  "Z" in box.get_text()]
        result = list(select_lines(text, *callbacks))
        assert len(result) == 0


class TestSelectCharacters():

    @pytest.fixture(autouse=True)
    def text(self, paragraphs):
        return paragraphs[0]

    @pytest.fixture(autouse=True)
    def boxes(self, text):
        return list(select_textboxes(text))

    @pytest.fixture(autouse=True)
    def lines(self, text):
        return list(select_lines(text))

    def setUp(self) -> None:
        self.test_page = self.test_paragraphs[0]
        self.test_boxes = list(select_textboxes(self.test_page))
        self.test_lines = list(select_lines(self.test_page))

    def test_returns_iterable(self, lines) -> None:
        result = select_characters(lines[0])
        assert isinstance(result, Iterable)

    def test_returns_characters_from_single_line(self, lines) -> None:
        characters = select_characters(lines[0])
        for character in characters:
            assert isinstance(character, LTChar)

    def test_returns_characters_from_multiple_lines(self, lines) -> None:
        characters = select_characters(lines)
        for character in characters:
            assert isinstance(character, LTChar)

    def test_returns_characters_from_single_textbox(self, boxes) -> None:
        characters = select_characters(boxes[0])
        for character in characters:
            assert isinstance(character, LTChar)

    def test_returns_characters_from_multiple_textboxes(self, boxes) -> None:
        characters = select_characters(boxes)
        for character in characters:
            assert isinstance(character, LTChar)

    def test_returns_characters_from_single_page(self, text) -> None:
        characters = select_characters(text)
        for character in characters:
            assert isinstance(character, LTChar)
        
    def test_returns_characters_from_multiple_pages(self, text) -> None:
        characters = select_characters(text)
        for character in characters:
            assert isinstance(character, LTChar)

    def test_filters_results_with_callback_function(self, text) -> None:
        callback = lambda char:  "v" in char.get_text()
        result = list(select_characters(text, callback))
        assert len(result) == 5

    def test_filters_results_with_multiple_callbacks(self, text) -> None:
        callbacks = [lambda box:  "v" in box.get_text(), lambda box: box.y0 > 550,  lambda box: box.y1 < 600]
        result = list(select_characters(text, *callbacks))
        assert len(result) == 1

    def test_returns_empty_list_when_no_matches_with_callback(self, text) -> None:
        callbacks = [lambda box:  "Z" in box.get_text()]
        result = list(select_lines(text, *callbacks))
        assert len(result) == 0

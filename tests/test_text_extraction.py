# Standard Imports
import re
import unittest

# Third-Party Imports
from pdfminer.layout import LTChar, LTPage, LTTextBoxHorizontal, LTTextLineHorizontal

# Local Imports
from helpers.selectors import extract_pages
from helpers.selectors import extract_textboxes
from helpers.selectors import extract_lines
from helpers.selectors import extract_characters


class TestPDFSelectors(unittest.TestCase):

    def setUp(self) -> None:
        self.test_pdf = open('tests/samples/sample_2.pdf', 'rb')

    def test_extract_pages_from_pdf(self) -> None:
        result = extract_pages(self.test_pdf)
        for page in result:
            self.assertIsInstance(page, LTPage)

    def test_extract_textboxes_from_single_pages(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            result = extract_textboxes(page)
            for textbox in result:
                self.assertIsInstance(textbox, LTTextBoxHorizontal)

    def test_extract_textboxes_from_multiple_pages(self) -> None:
        pages = extract_pages(self.test_pdf)
        result = extract_textboxes(pages)
        for textbox in result:
            self.assertIsInstance(textbox, LTTextBoxHorizontal)

    def test_extract_lines_from_single_textboxs(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            for textbox in textboxes:
                result = extract_lines(textbox)
                for line in result:
                    self.assertIsInstance(line, LTTextLineHorizontal)

    def test_extract_lines_from_multiple_boxes(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            result = extract_lines(textboxes)
            for line in result:
                self.assertIsInstance(line, LTTextLineHorizontal)
    
    def test_extract_lines_from_single_pages(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            result = extract_lines(page)
            for line in result:
                self.assertIsInstance(line, LTTextLineHorizontal)
    
    def test_extract_lines_from_multiple_pages(self) -> None:
        pages = extract_pages(self.test_pdf)
        result = extract_lines(pages)
        for line in result:
            self.assertIsInstance(line, LTTextLineHorizontal)

    def test_extract_characters_from_single_lines(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            for textbox in textboxes:
                lines = extract_lines(textbox)
                for line in lines:
                    characters = extract_characters(line)
                    for character in characters:
                        self.assertIsInstance(character, LTChar)

    def test_extract_characters_from_multiple_lines(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            for textbox in textboxes:
                lines = extract_lines(textbox)
                characters = extract_characters(lines)
                for character in characters:
                    self.assertIsInstance(character, LTChar)
    
    def test_extract_characters_from_single_textboxes(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            for textbox in textboxes:
                characters = extract_characters(textbox)
                for character in characters:
                    self.assertIsInstance(character, LTChar)

    def test_extract_characters_from_multiple_textboxes(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            textboxes = extract_textboxes(page)
            characters = extract_characters(textboxes)
            for character in characters:
                self.assertIsInstance(character, LTChar)
    
    def test_extract_characters_from_single_pages(self) -> None:
        pages = extract_pages(self.test_pdf)
        for page in pages:
            characters = extract_characters(page)
            for character in characters:
                self.assertIsInstance(character, LTChar)
        
    def test_extract_characters_from_multiple_pages(self) -> None:
        pages = extract_pages(self.test_pdf)
        characters = extract_characters(pages)
        for character in characters:
            self.assertIsInstance(character, LTChar)

    def tearDown(self) -> None:
        self.test_pdf.close()

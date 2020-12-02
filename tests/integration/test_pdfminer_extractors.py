# tests/integration/test_pdfminer_extractors.py

# Standard Imports
import os
from typing import Generator

# Third-Party Imports
from pdfminer.layout import LTPage
import pytest

# Local Imports
from parser.pdfminer.extractors import extract_pages


SAMPLES = 'tests/samples/'


class TestExtractingPages():

    @pytest.fixture(autouse=True)
    def test_paragraphs(self) -> None:
        file = open(os.path.join(SAMPLES, '01_paragraphs.pdf'), 'rb')
        yield file
        file.close()

    @pytest.fixture(autouse=True)
    def test_pages(self) -> None:
        file = open(os.path.join(SAMPLES, '02_multiple_pages.pdf'), 'rb')
        yield file
        file.close()

    def test_returns_iterator(self, test_paragraphs) -> None:
        result = extract_pages(test_paragraphs)
        assert isinstance(result, Generator)

    def test_returns_pages_from_pdf(self, test_paragraphs) -> None:
        result = extract_pages(test_paragraphs)
        for page in result:
            assert isinstance(page, LTPage)
    
    def test_returns_correct_number_of_pages(self, test_pages) -> None:
        result = list(extract_pages(test_pages))
        assert len(result) == 3

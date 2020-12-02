# tests/conftest.py

# Standard Imports
import os

# Third -Party Imports
from pdfminer.high_level import extract_pages
import pytest


SAMPLES = 'tests/samples/'


@pytest.fixture(scope="module")
def paragraphs():
    with open(os.path.join(SAMPLES, '01_paragraphs.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="module")
def multiple_pages():
    with open(os.path.join(SAMPLES, '02_multiple_pages.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="module")
def table_borders():
    with open(os.path.join(SAMPLES, '03_table_borders.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="module")
def missing_values():
    with open(os.path.join(SAMPLES, '04_missing_values.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="module")
def text_alignment():
    with open(os.path.join(SAMPLES, '05_text_alignment.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="module")
def table_headers():
    with open(os.path.join(SAMPLES, '06_table_headers.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="module")
def table_titles():
    with open(os.path.join(SAMPLES, '07_table_titles.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="module")
def embedded_tables():
    with open(os.path.join(SAMPLES, '08_embedded_tables.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))

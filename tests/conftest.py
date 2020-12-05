# tests/conftest.py

# Standard Imports
import os

# Third -Party Imports
from pdfminer.high_level import extract_pages
import pytest


SAMPLES = 'tests/samples/'


@pytest.fixture(scope="package")
def pages():
    with open(os.path.join(SAMPLES, '00_pages.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def text():
    with open(os.path.join(SAMPLES, '01_text.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def fonts():
    with open(os.path.join(SAMPLES, '02_fonts.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def paragraphs():
    with open(os.path.join(SAMPLES, '03_paragraphs.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def table_borders():
    with open(os.path.join(SAMPLES, '05_table_borders.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def missing_values():
    with open(os.path.join(SAMPLES, '06_missing_values.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def text_alignment():
    with open(os.path.join(SAMPLES, '07_table_alignment.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


# @pytest.fixture(scope="package")
# def data_types():
#     with open(os.path.join(SAMPLES, '06_data_types.pdf'), 'rb') as pdf:
#         return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def table_headers():
    with open(os.path.join(SAMPLES, '09_table_headers.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def table_titles():
    with open(os.path.join(SAMPLES, '10_table_titles.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def embedded_tables():
    with open(os.path.join(SAMPLES, '11_embedded_tables.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))


@pytest.fixture(scope="package")
def page_overflow():
    with open(os.path.join(SAMPLES, '12_page_overflow.pdf'), 'rb') as pdf:
        return list(extract_pages(pdf))

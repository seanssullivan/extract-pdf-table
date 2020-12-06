# helpers/pdfminer/extractors/tables.py

# Standard Imports
from functools import reduce
import logging
from typing import Dict, Iterable, List, Text, Tuple, Union

# Third-Party Imports
import pandas as pd
from pdfminer.layout import LTPage, LTContainer

# Local Imports
from .. import callbacks as cb
from ..analyzers.divisions import determine_column_positions, determine_row_positions
from ..selectors import select_lines


def extract_table(container: Union[LTPage, Iterable[LTPage]], headers: int = 1) -> pd.DataFrame:
    """Extract tabulated data from PDF page(s)."""

    # Ensure argument is an LTPage object
    if isinstance(container, LTPage):
        table = _extract_table_from_page(container, headers)
    
    elif isinstance(container, Iterable):
        dataframes = [extract_table(page, headers=headers) for page in container if isinstance(page, LTPage)]
        table = pd.concat(dataframes, ignore_index=True)
    
    # otherwise return an empty list
    else:
        raise TypeError(f"{type(container)!s} is not a valid argument type")
    
    return table


def _extract_table_from_page(page: LTPage, headers: int = 1) -> pd.DataFrame:
    """Extract tabulated data from a PDF page.

    This function is designed to help extract tables
    and should not be imported into other modules."""

    # Determine positions of rows and columns
    rows = determine_row_positions(page)
    cols = determine_column_positions(page)
    
    # Extract field names
    fields = extract_field_names(page, rows, cols, headers)

    # Extract table entries
    table_entries = []
    for row in rows[headers:]:
        table_entry = extract_table_entry(page, row, cols, fields)
        table_entries.append(table_entry)
    
    # Convert table entries into DataFrame
    table = pd.DataFrame(table_entries)
    return table


def extract_field_names(container: LTContainer, rows: List, columns: List, headers: int = 1) -> pd.Index:
    """Return the field names found inside the header rows."""
    # If there are no headers, assign each field a number
    if headers == 0:
        return range(len(columns))

    # If header takes up multiple lines, merge them
    if headers > 1:
        coordinates = list(zip(*rows[headers - 1]))
        header_row = (min(coordinates[0]), max(coordinates[1]))
    else:
        header_row = rows[0]

    # Extract field names from the header row
    field_names = extract_row_content(container, header_row, columns)

    return pd.Index(field_names)


def extract_table_entry(container: LTContainer, row: Tuple, columns: List, field_names: List) -> Dict:
    """Return a dictionary containing each field and value from the row of a table."""

    # Extract row content and assign a field to each cell
    cells = extract_row_content(container, row, columns)
    entry = {field: content for field, content in zip(field_names, cells)}

    return entry


def extract_column_content(container: LTContainer, column: Tuple, rows: List) -> List:
    """Return the content of LTTextLineHorizontal objects inside a table column."""
    # Select cells inside the table column and extract their content
    content = []
    for row in rows:
        cell = extract_cell_content(container, (column[0], row[0], column[1], row[1]))
        content.append(cell)

    return content


def extract_row_content(container: LTContainer, row: Tuple, columns: List) -> List:
    """Return the content of LTTextLineHorizontal objects inside a table row."""
    # Select cells inside the table row and extract their content
    content = []
    for col in columns:
        cell = extract_cell_content(container, (col[0], row[0], col[1], row[1]))
        content.append(cell)

    return content


def extract_cell_content(container: LTContainer, bbox: Tuple) -> Text:
    """Return the content of LTTextLineHorizontal objects inside a table cell."""
    # Select lines inside the table cell and combine their content
    lines = select_lines(container, cb.within(bbox, margin=1))
    content = reduce(lambda acc, ln: (acc + ln.get_text()), lines, "").strip()
    return content

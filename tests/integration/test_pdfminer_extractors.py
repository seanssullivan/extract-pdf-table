# tests/integration/test_pdfminer_extractors.py

# Standard Imports
import os
from typing import Generator

# Third-Party Imports
import pandas as pd
from pdfminer.layout import LTPage
import pytest

# Local Imports
from parser.pdfminer.extractors.pages import extract_pages
from parser.pdfminer.extractors.tables import extract_cell_content
from parser.pdfminer.extractors.tables import extract_column_content
from parser.pdfminer.extractors.tables import extract_row_content
from parser.pdfminer.extractors.tables import extract_table_entry
from parser.pdfminer.extractors.tables import extract_field_names
from parser.pdfminer.extractors.tables import extract_table


SAMPLES = 'tests/samples/'


class TestExtractingPages():

    @pytest.fixture(autouse=True)
    def test_pages(self) -> None:
        file = open(os.path.join(SAMPLES, '00_pages.pdf'), 'rb')
        yield file
        file.close()

    def test_returns_iterator(self, test_pages) -> None:
        result = extract_pages(test_pages)
        assert isinstance(result, Generator)

    def test_returns_pages_from_pdf(self, test_pages) -> None:
        result = extract_pages(test_pages)
        for page in result:
            assert isinstance(page, LTPage)
    
    def test_returns_correct_number_of_pages(self, test_pages) -> None:
        result = list(extract_pages(test_pages))
        assert len(result) == 3


class TestExtractCellContent():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def borders(self, request, table_borders):
        yield table_borders[request.param]

    def test_returns_text(self, table_borders) -> None:
        result = extract_cell_content(table_borders[0], (72.5, 706.0, 164.0, 719.5))
        assert isinstance(result, str)

    def test_returns_correct_text(self, borders) -> None:
        result = extract_cell_content(borders, (259.6, 706.0, 352.7, 719.5))
        assert result == 'TestField1'


class TestExtractColumnContent():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def borders(self, request, table_borders):
        yield table_borders[request.param]

    def test_returns_list(self, table_borders) -> None:
        column, rows = (72.5, 164.0), [(706.0, 719.5), (692.2, 705.5), (678.2, 691.7), (664.2, 677.7), (650.2, 663.7), (636.5, 649.7)]
        result = extract_column_content(table_borders[0], column, rows)
        assert isinstance(result, list)

    def test_returns_correct_text(self, borders) -> None:
        column, rows = (72.5, 164.0), [(706.0, 719.5), (692.2, 705.5), (678.2, 691.7), (664.2, 677.7), (650.2, 663.7), (636.5, 649.7)]
        expected = ["IdField", "1", "2", "3", "4", "5"]
        actual = extract_column_content(borders, column, rows)
        assert actual == expected


class TestExtractRowContent():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def borders(self, request, table_borders):
        yield table_borders[request.param]

    def test_returns_list(self, table_borders) -> None:
        row, columns = (706.0, 719.5), [(72.5, 164.0), (164.5, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        result = extract_row_content(table_borders[0], row, columns)
        assert isinstance(result, list)

    def test_returns_correct_text(self, borders) -> None:
        row, columns = (706.0, 719.5), [(72.5, 164.0), (164.5, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        expected = ["IdField", "NameField", "TestField1", "TestField2", "TestField3"]
        actual = extract_row_content(borders, row, columns)
        assert actual == expected


class TestExtractTableEntry():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def borders(self, request, table_borders):
        yield table_borders[request.param]

    def test_returns_dict(self, table_borders) -> None:
        fields = ["IdField", "NameField", "TestField1", "TestField2", "TestField3"]
        row, columns = (692.2, 705.5), [(72.5, 164.0), (164.6, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        result = extract_table_entry(table_borders[0], row, columns, fields)
        assert isinstance(result, dict)

    def test_returns_correct_text(self, borders) -> None:
        fields = ["IdField", "NameField", "TestField1", "TestField2", "TestField3"]
        row, columns = (692.2, 705.5), [(72.5, 164.0), (164.6, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        expected = {"IdField": "1", "NameField": "Name1", "TestField1": "Value1", "TestField2": "Value2", "TestField3": "Value3"}
        actual = extract_table_entry(borders, row, columns, fields)
        assert actual == expected


class TestExtractFieldNames():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def borders(self, request, table_borders):
        yield table_borders[request.param]

    def test_returns_pandas_index(self, table_borders) -> None:
        rows = [(706.0, 719.5), (692.2, 705.5), (678.2, 691.7), (664.2, 677.7), (650.2, 663.7), (636.5, 649.7)]
        cols = [(72.5, 164.0), (164.6, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        result = extract_field_names(table_borders[0], rows, cols, headers=1)
        assert isinstance(result, pd.Index)

    def test_returns_correct_text(self, borders) -> None:
        rows = [(706.0, 719.5), (692.2, 705.5), (678.2, 691.7), (664.2, 677.7), (650.2, 663.7), (636.5, 649.7)]
        cols = [(72.5, 164.0), (164.6, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        actual = extract_field_names(borders, rows, cols, headers=1)
        expected = pd.Index(["IdField", "NameField", "TestField1", "TestField2", "TestField3"])
        pd.testing.assert_index_equal(actual, expected)


class TestExtractingTable():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def borders(self, request, table_borders):
        yield table_borders[request.param]
    
    def test_returns_dataframe(self, table_borders) -> None:
        result = extract_table(table_borders[0])
        assert isinstance(result, pd.DataFrame)

    # def test_returns_none_if_no_tables_found(self, test_paragraphs) -> None:
    #     result = extract_table(test_paragraphs[0])
    #     assert not result

    def test_returns_correct_table_data_when_working_with_borders(self, borders) -> None:
        actual = extract_table(borders)
        expected = pd.DataFrame(
            columns=['IdField', 'NameField', 'TestField1', 'TestField2', 'TestField3'],
            data=[["1", 'Name1', 'Value1', 'Value2', 'Value3'],
                  ["2", 'Name2', 'Value4', 'Value5', 'Value6'],
                  ["3", 'Name3', 'Value7', 'Value8', 'Value9'],
                  ["4", 'Name4', 'Value10', 'Value11', 'Value12'],
                  ["5", 'Name5', 'Value13', 'Value14', 'Value15']]
        )
        pd.testing.assert_frame_equal(actual, expected)

    def test_returns_correct_table_when_not_missing_values(self, missing_values) -> None:
        actual = extract_table(missing_values[0])
        expected = pd.DataFrame(
            columns=['IdField', 'NameField', 'TestField1', 'TestField2', 'TestField3'],
            data=[["1", 'Name1', 'Value1', 'Value2', 'Value3'],
                  ["2", 'Name2', 'Value4', 'Value5', 'Value6'],
                  ["3", 'Name3', 'Value7', 'Value8', 'Value9'],
                  ["4", 'Name4', 'Value10', 'Value11', 'Value12'],
                  ["5", 'Name5', 'Value13', 'Value14', 'Value15']]
        )
        pd.testing.assert_frame_equal(actual, expected)

    def test_returns_correct_table_when_missing_some_values(self, missing_values) -> None:
        actual = extract_table(missing_values[1])
        expected = pd.DataFrame(
            columns=['IdField', 'NameField', 'TestField1', 'TestField2', 'TestField3'],
            data=[["1", 'Name1', 'Value1', 'Value2', 'Value3'],
                  ["2", 'Name2', 'Value4', 'Value5', ''],
                  ["3", 'Name3', 'Value6', 'Value7', 'Value8'],
                  ["4", 'Name4', 'Value9', '', ''],
                  ["5", 'Name5', 'Value10', 'Value11', 'Value12']]
        )
        pd.testing.assert_frame_equal(actual, expected)

    def test_returns_correct_table_when_missing_more_values(self, missing_values) -> None:
        actual = extract_table(missing_values[2])
        expected = pd.DataFrame(
            columns=['IdField', 'NameField', 'TestField1', 'TestField2', 'TestField3'],
            data=[["1", 'Name1', 'Value1', '', 'Value2'],
                  ["2", 'Name2', 'Value3', 'Value4', ''],
                  ["3", 'Name3', '', 'Value5', 'Value6'],
                  ["4", 'Name4', 'Value7', '', 'Value8'],
                  ["5", 'Name5', '', 'Value9', '']]
        )
        pd.testing.assert_frame_equal(actual, expected)
    
    def test_returns_correct_table_when_missing_many_values(self, missing_values) -> None:
        actual = extract_table(missing_values[3])
        expected = pd.DataFrame(
            columns=['IdField', 'NameField', 'TestField1', 'TestField2', 'TestField3'],
            data=[["1", 'Name1', 'Value1', '', 'Value2'],
                  ["2", 'Name2', 'Value3', '', ''],
                  ["3", 'Name3', '', 'Value4', ''],
                  ["4", 'Name4', 'Value5', '', ''],
                  ["5", 'Name5', '', '', 'Value6']]
        )
        pd.testing.assert_frame_equal(actual, expected)

    def test_returns_correct_table_when_missing_most_values(self, missing_values) -> None:
        actual = extract_table(missing_values[4])
        expected = pd.DataFrame(
            columns=['IdField', 'NameField', 'TestField1', 'TestField2', 'TestField3'],
            data=[["1", 'Name1', 'Value1', '', ''],
                  ["2", 'Name2', '', '', 'Value2'],
                  ["3", 'Name3', '', '', ''],
                  ["4", 'Name4', '', 'Value3', ''],
                  ["5", 'Name5', '', '', '']]
        )
        pd.testing.assert_frame_equal(actual, expected)

    def test_returns_tables_that_span_multiple_pages(self, page_overflow) -> None:
        result = extract_table(page_overflow[0:3])
        assert result.shape == (100, 5)
        pd.testing.assert_index_equal(
            result.columns, 
            pd.Index(['IdField', 'NameField', 'TestField1', 'TestField2', 'TestField3'])
        )

    # def test_returns_tables_on_multiple_pages_without_repeating_headers(self, page_overflow) -> None:
    #     result = extract_table(page_overflow[3:6])
    #     assert result.shape == (100, 5)
    #     pd.testing.assert_index_equal(
    #         result.columns, 
    #         pd.Index(['IdField', 'NameField', 'TestField1', 'TestField2', 'TestField3'])
    #     )

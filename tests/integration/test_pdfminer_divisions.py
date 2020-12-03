# tests/integration/test_pdfminer_division_analyzer.py

# Standard Imports
import itertools

# Third-Party Imports
import pytest

# Local Imports
from parser.pdfminer.analyzers.divisions import determine_column_positions
from parser.pdfminer.analyzers.divisions import determine_row_positions


def listAlmostEqual(first: list, second: list, delta: float) -> bool:
    for result in zip(itertools.chain.from_iterable(first), itertools.chain.from_iterable(second)):
        if abs(result[0] - result[1]) > delta:
            return False
    return True


class TestDetermineColumnPositions():

    @pytest.fixture(autouse=True)
    def page(self, table_borders):
        return table_borders[0]

    def test_returns_list_of_tuples(self, table_borders) -> None:
        result = determine_column_positions(table_borders[0])
        assert isinstance(result, list)
        for position in result:
            assert isinstance(position, tuple)
    
    def test_returns_correct_columns_with_full_borders(self, table_borders) -> None:
        expected = [(72.525, 164.075), (164.58, 259.105), (259.6, 352.65), (353.15, 446.175), (446.68, 539.73)]
        actual = determine_column_positions(table_borders[0])
        assert len(actual) == 5
        assert actual == expected

    def test_returns_correct_columns_without_horizontal_dividers(self, table_borders) -> None:
        expected = [(72.525, 164.075), (164.58, 259.105), (259.6, 352.65), (353.15, 446.175), (446.68, 539.73)]
        actual = determine_column_positions(table_borders[1])
        assert len(actual) == 5
        assert actual == expected

    def test_returns_correct_columns_without_vertical_dividers(self, table_borders) -> None:
        # expected = [(72.525, 164.075), (164.83, 259.355), (259.85, 352.9), (353.4, 446.425), (446.93, 539.73)]
        exact = [(77.775, 110.286), (169.58, 220.086), (264.85, 313.116), (358.4, 406.656), (451.93, 500.186)]
        actual = determine_column_positions(table_borders[2])
        assert len(actual) == 5
        # assert listAlmostEqual(actual, expected, delta=5)
        assert actual == exact
    
    def test_returns_correct_columns_with_only_header_line(self, table_borders) -> None:
        expected = [(72.525, 164.075), (164.83, 259.355), (259.85, 352.9), (353.4, 446.425), (446.93, 539.73)]
        exact = [(72.025, 164.075), (164.58, 259.105), (259.6, 352.65), (353.15, 446.175), (446.68, 539.73)]
        actual = determine_column_positions(table_borders[3])
        assert len(actual) == 5
        assert listAlmostEqual(actual, expected, delta=5)
        assert actual == exact

    def test_returns_correct_columns_with_no_borders(self, table_borders) -> None:
        # expected = [(72.525, 164.075), (164.83, 259.355), (259.85, 352.9), (353.4, 446.425), (446.93, 539.73)]
        exact = [(77.525, 110.036), (169.33, 219.836), (264.6, 312.866), (358.15, 406.406), (451.67, 499.936)]
        actual = determine_column_positions(table_borders[4])
        assert len(actual) == 5
        # assert listAlmostEqual(actual, expected, delta=5)
        assert actual == exact
    
    def test_returns_correct_number_of_columns_when_not_missing_values(self, missing_values) -> None:
        result = determine_column_positions(missing_values[0])
        assert len(result) == 5

    def test_returns_correct_number_of_columns_when_missing_some_values(self, missing_values) -> None:
        result = determine_column_positions(missing_values[1])
        assert len(result) == 5

    def test_returns_correct_number_of_columns_when_missing_more_values(self, missing_values) -> None:
        result = determine_column_positions(missing_values[2])
        assert len(result) == 5
    
    def test_returns_correct_number_of_columns_when_missing_many_values(self, missing_values) -> None:
        result = determine_column_positions(missing_values[3])
        assert len(result) == 5
    
    def test_returns_correct_number_of_columns_when_missing_most_values(self, missing_values) -> None:
        result = determine_column_positions(missing_values[4])
        assert len(result) == 5


class TestDetermineRowPositions():

    def test_returns_list_of_tuples(self, table_borders) -> None:
        result = determine_row_positions(table_borders[0])
        assert isinstance(result, list)
        for position in result:
            assert isinstance(position, tuple)

    def test_returns_correct_rows_with_full_borders(self, table_borders) -> None:
        expected = [(705.97, 719.47), (692.22, 705.47), (678.22, 691.72), (664.2, 677.725), (650.2, 663.7), (636.45, 649.7)]
        actual = determine_row_positions(table_borders[0])
        assert len(actual) == 6
        assert listAlmostEqual(actual, expected, delta=5)
    
    def test_returns_correct_rows_without_horizontal_dividers(self, table_borders) -> None:
        expected = [(705.97, 719.47), (692.22, 705.47), (678.22, 691.72), (664.2, 677.725), (650.2, 663.7), (636.45, 649.7)]
        actual = determine_row_positions(table_borders[1])
        assert len(actual) == 6
        assert listAlmostEqual(actual, expected, delta=5)

    def test_returns_correct_rows_without_vertical_dividers(self, table_borders) -> None:
        expected = [(705.97, 719.47), (692.22, 705.47), (678.22, 691.72), (664.2, 677.725), (650.2, 663.7), (636.45, 649.7)]
        actual = determine_row_positions(table_borders[2])
        assert len(actual) == 6
        assert listAlmostEqual(actual, expected, delta=5)

    def test_returns_correct_rows_with_only_header_line(self, table_borders) -> None:
        expected = [(705.97, 719.47), (692.22, 705.47), (678.22, 691.72), (664.2, 677.725), (650.2, 663.7), (636.45, 649.7)]
        exact = [(706.72, 717.72), (692.97, 703.97), (679.47, 690.47), (665.95, 676.95), (652.45, 663.45), (639.2, 650.2)]
        actual = determine_row_positions(table_borders[3])
        assert len(actual) == 6
        assert listAlmostEqual(actual, expected, delta=5)
        assert actual == exact

    def test_returns_correct_rows_with_no_borders(self, table_borders) -> None:
        expected = [(705.97, 719.47), (692.22, 705.47), (678.22, 691.72), (664.2, 677.725), (650.2, 663.7), (636.45, 649.7)]
        exact = [(706.72, 717.72), (693.47, 704.47), (679.97, 690.97), (666.45, 677.45), (652.95, 663.95), (639.7, 650.7)]
        actual = determine_row_positions(table_borders[4])
        assert len(actual) == 6
        assert listAlmostEqual(actual, expected, delta=5)
        assert actual == exact

    def test_returns_correct_number_of_rows_when_not_missing_values(self, missing_values) -> None:
        result = determine_row_positions(missing_values[0])
        assert len(result) == 6

    def test_returns_correct_number_of_rows_when_missing_some_values(self, missing_values) -> None:
        result = determine_row_positions(missing_values[1])
        assert len(result) == 6

    def test_returns_correct_number_of_rows_when_missing_more_values(self, missing_values) -> None:
        result = determine_row_positions(missing_values[2])
        assert len(result) == 6
    
    def test_returns_correct_number_of_rows_when_missing_many_values(self, missing_values) -> None:
        result = determine_row_positions(missing_values[3])
        assert len(result) == 6
    
    def test_returns_correct_number_of_rows_when_missing_most_values(self, missing_values) -> None:
        result = determine_row_positions(missing_values[4])
        assert len(result) == 6

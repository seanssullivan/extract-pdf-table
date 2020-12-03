# tests/integration/test_pdfminer_division_analyzer.py

# Standard Imports
import itertools

# Third-Party Imports
import pytest

# Local Imports
from parser.pdfminer.analyzers.divisions import determine_column_positions
from parser.pdfminer.analyzers.divisions import determine_row_positions


def positionAlmostEqual(first: list, second: list, delta: float) -> bool:
    positions = [zip(*column) for column in zip(first, second)]
    for left_sides, right_sides in positions:
        first_side, second_side = min(left_sides, right_sides, key=lambda s: abs(s[0] - s[1]))
        diff = abs(first_side - second_side)
        if diff > delta:
            raise AssertionError(f'{first_side} != {second_side} within {delta} delta ({diff} difference)')
    return True


class TestDetermineColumnPositions():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def borders(self, request, table_borders):
        yield table_borders[request.param]

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def values(self, request, missing_values):
        yield missing_values[request.param]

    def test_returns_list_of_tuples(self, table_borders) -> None:
        result = determine_column_positions(table_borders[0])
        assert isinstance(result, list)
        for position in result:
            assert isinstance(position, tuple)

    def test_returns_correct_columns_when_working_with_borders(self, borders) -> None:
        expected = [(72.525, 164.075), (164.58, 259.105), (259.6, 352.65), (353.15, 446.175), (446.68, 539.73)]
        actual = determine_column_positions(borders)
        assert positionAlmostEqual(actual, expected, delta=10)
    
    def test_returns_correct_columns_when_dealing_with_missing_values(self, values) -> None:
        expected = [(72.525, 164.075), (164.58, 259.105), (259.6, 352.65), (353.15, 446.175), (446.68, 539.73)]
        actual = determine_column_positions(values)
        assert positionAlmostEqual(actual, expected, delta=10)


class TestDetermineRowPositions():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def borders(self, request, table_borders):
        yield table_borders[request.param]

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def values(self, request, missing_values):
        yield missing_values[request.param]

    def test_returns_list_of_tuples(self, table_borders) -> None:
        result = determine_row_positions(table_borders[0])
        assert isinstance(result, list)
        for position in result:
            assert isinstance(position, tuple)

    def test_returns_correct_rows_when_working_with_borders(self, borders) -> None:
        expected = [(705.97, 719.47), (692.22, 705.47), (678.22, 691.72), (664.2, 677.725), (650.2, 663.7), (636.45, 649.7)]
        actual = determine_row_positions(borders)
        assert positionAlmostEqual(actual, expected, delta=5)
    
    def test_returns_correct_rows_when_dealing_with_missing_values(self, values) -> None:
        expected = [(705.97, 719.47), (692.22, 705.47), (678.22, 691.72), (664.2, 677.725), (650.2, 663.7), (636.45, 649.7)]
        actual = determine_row_positions(values)
        assert positionAlmostEqual(actual, expected, delta=5)

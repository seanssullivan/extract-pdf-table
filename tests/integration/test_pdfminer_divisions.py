# tests/integration/test_pdfminer_division_analyzer.py

# Third-Party Imports
import pytest

# Local Imports
from parser.pdfminer.analyzers.divisions import determine_column_positions
from parser.pdfminer.analyzers.divisions import determine_row_positions


def positionsAlmostEqual(first: list, second: list, delta: float) -> bool:
    positions = [zip(*column) for column in zip(first, second)]
    for left_sides, right_sides in positions:
        first_side, second_side = min(left_sides, right_sides, key=lambda s: abs(s[0] - s[1]))
        diff = abs(first_side - second_side)
        if diff > delta:
            raise AssertionError(f'{first_side} != {second_side} within {delta} delta ({diff} difference)')
    return True


class TestDetermineColumnPositions():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def column(self, request, columns):
        yield columns[request.param]

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def border(self, request, table_borders):
        yield table_borders[request.param]

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def values(self, request, missing_values):
        yield missing_values[request.param]

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def alignment(self, request, text_alignment):
        yield text_alignment[request.param]

    def test_returns_list_of_tuples(self, columns) -> None:
        result = determine_column_positions(columns[0])
        assert isinstance(result, list)
        for position in result:
            assert isinstance(position, tuple)

    def test_returns_the_expected_number_of_column_positions(self, column) -> None:
        expected = column.pageid  # sample file has same number of columns per page as the page number
        result = determine_column_positions(column)
        assert len(result) == expected
        
    def test_returns_correct_column_positions_when_working_with_borders(self, border) -> None:
        expected = [(72.5, 164.0), (164.5, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        actual = determine_column_positions(border)
        assert positionsAlmostEqual(actual, expected, delta=10)
    
    def test_returns_correct_column_positions_when_working_with_missing_values(self, values) -> None:
        expected = [(72.5, 164.0), (164.5, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        actual = determine_column_positions(values)
        assert positionsAlmostEqual(actual, expected, delta=10)

    def test_returns_correct_column_positions_when_working_with_different_alignments(self, alignment) -> None:
        expected = [(72.5, 135.6), (136.1, 259.1), (259.6, 352.7), (353.2, 446.2), (446.7, 539.7)]
        actual = determine_column_positions(alignment)
        assert positionsAlmostEqual(actual, expected, delta=10)


class TestDetermineRowPositions():

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def border(self, request, table_borders):
        yield table_borders[request.param]

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def values(self, request, missing_values):
        yield missing_values[request.param]

    @pytest.fixture(scope="function", params=[i for i in range(5)])
    def alignment(self, request, text_alignment):
        yield text_alignment[request.param]

    def test_returns_list_of_tuples(self, table_borders) -> None:
        result = determine_row_positions(table_borders[0])
        assert isinstance(result, list)
        for position in result:
            assert isinstance(position, tuple)

    def test_returns_correct_row_positions_when_working_with_borders(self, border) -> None:
        expected = [(706.0, 719.5), (692.2, 705.5), (678.2, 691.7), (664.2, 677.7), (650.2, 663.7), (636.5, 649.7)]
        actual = determine_row_positions(border)
        assert positionsAlmostEqual(actual, expected, delta=5)
    
    def test_returns_correct_row_positions_when_working_with_missing_values(self, values) -> None:
        expected = [(706.0, 719.5), (692.2, 705.5), (678.2, 691.7), (664.2, 677.7), (650.2, 663.7), (636.5, 649.7)]
        actual = determine_row_positions(values)
        assert positionsAlmostEqual(actual, expected, delta=5)

    def test_returns_correct_row_positions_when_working_with_different_alignments(self, alignment) -> None:
        expected = [(706.0, 719.5), (692.2, 705.5), (678.2, 691.7), (664.2, 677.7), (650.2, 663.7), (636.5, 649.7)]
        actual = determine_row_positions(alignment)
        assert positionsAlmostEqual(actual, expected, delta=5)

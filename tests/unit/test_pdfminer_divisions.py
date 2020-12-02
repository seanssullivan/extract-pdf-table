# tests/unit/test_layout_divisions.py

# Local Imports
from parser.pdfminer.analyzers.divisions import determine_column_positions
from parser.pdfminer.analyzers.divisions import determine_row_positions


class TestDetermineColumnPositions():

    def test_returns_list_of_tuples(self) -> None:
        test_positions = [(0, 0, 10, 10), (10, 10, 10, 10)]
        result = determine_column_positions(*test_positions)
        assert isinstance(result, list)
        assert all(map(lambda e: isinstance(e, tuple), result))

    def test_returns_correct_column_positions(self) -> None:
        test_positions = [
            (0, 0, 10, 10), (15, 0, 25, 10), (30, 0, 40, 10), (45, 0, 55, 10), (60, 0, 70, 10),
            (0, 15, 10, 25), (15, 15, 25, 25), (30, 15, 40, 25), (45, 15, 55, 25), (60, 15, 70, 25),
            (0, 30, 10, 40), (15, 30, 25, 40), (30, 30, 40, 40), (45, 30, 55, 40), (60, 30, 70, 40),
            (0, 45, 10, 55), (15, 45, 25, 55), (30, 45, 40, 55), (45, 45, 55, 55), (60, 45, 70, 55),
            (0, 60, 10, 70), (15, 60, 25, 70), (30, 60, 40, 70), (45, 60, 55, 70), (60, 60, 70, 70),
        ]
        actual = determine_column_positions(*test_positions)
        expected = [(0, 10), (15, 25), (30, 40), (45, 55), (60, 70)]
        assert actual == expected

    def test_returns_atleast_one_column(self) -> None:
        test_positions = [(5, 0, 25, 10), (0, 15, 20, 25), (5, 30, 25, 40), (0, 45, 20, 55), (5, 60, 25, 70)]
        actual = determine_column_positions(*test_positions)
        expected = [(0, 25)]
        assert len(actual) == 1
        assert actual == expected


class TestDetermineRowPositions():

    def test_returns_list_of_tuples(self) -> None:
        test_positions = [(0, 0, 10, 10), (10, 10, 10, 10)]
        result = determine_row_positions(*test_positions)
        assert isinstance(result, list)
        assert all(map(lambda e: isinstance(e, tuple), result))

    def test_returns_correct_row_positions(self) -> None:
        test_positions = [
            (0, 0, 10, 10), (15, 0, 25, 10), (30, 0, 40, 10), (45, 0, 55, 10), (60, 0, 70, 10),
            (0, 15, 10, 25), (15, 15, 25, 25), (30, 15, 40, 25), (45, 15, 55, 25), (60, 15, 70, 25),
            (0, 30, 10, 40), (15, 30, 25, 40), (30, 30, 40, 40), (45, 30, 55, 40), (60, 30, 70, 40),
            (0, 45, 10, 55), (15, 45, 25, 55), (30, 45, 40, 55), (45, 45, 55, 55), (60, 45, 70, 55),
            (0, 60, 10, 70), (15, 60, 25, 70), (30, 60, 40, 70), (45, 60, 55, 70), (60, 60, 70, 70),
        ]
        actual = determine_row_positions(*test_positions)
        expected = [(60, 70), (45, 55), (30, 40), (15, 25), (0, 10)]
        assert actual == expected

    def test_returns_atleast_one_row(self) -> None:
        test_positions = [(0, 5, 10, 25), (15, 0, 25, 20), (30, 5, 40, 25), (45, 0, 55, 20), (60, 5, 70, 25)]
        actual = determine_row_positions(*test_positions)
        expected = [(0, 25)]

        assert len(actual) == 1
        assert actual == expected

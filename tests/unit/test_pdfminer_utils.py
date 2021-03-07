# tests/unit/test_pdfminer_utils.py

# Local Imports
from src.pdfminer.utils import positions
from src.pdfminer.utils import merge_overlapping_positions


class TestMergeOverlappingPositions():

    def test_returns_list_of_positions(self):
        result = merge_overlapping_positions(*[(0, 1), (2, 3), (4, 5)])
        assert isinstance(result, list)
        for position in result:
            assert isinstance(position, tuple)

    def test_returns_unique_positions(self):
        result = merge_overlapping_positions(*[
            (0, 10), (5, 10), (15, 25), (20, 25), (30, 40), (35, 45), (50, 60), (55, 65)
        ])
        assert len(result) == len(set(result))

    def test_returns_correct_positions(self):
        expected = [(72.025, 72.525), (539.73, 540.23)]
        actual = merge_overlapping_positions(*[
            (72.025, 72.525), (539.73, 540.23),
            (72.025, 72.525), (539.73, 540.23),
            (72.025, 72.525), (539.73, 540.23),
            (72.025, 72.525), (539.73, 540.23),
            (72.025, 72.525), (539.73, 540.23),
            (72.025, 72.525), (539.73, 540.23)
        ])
        assert actual == expected

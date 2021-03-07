# tests/integration/test_pdfminer_sections.py

# Standard Imports
import itertools

# Third-Party Imports
import pytest

# Local Imports
from src.pdfminer.analyzers.sections import determine_header_positions


def listAlmostEqual(first: list, second: list, delta: float = ...) -> None:
    for idx, result in enumerate(zip(itertools.chain.from_iterable(first), itertools.chain.from_iterable(second))):
        accuracy = delta + 50 if idx == 2 else delta
        if abs(result[0] - result[1]) > accuracy:
            return False
    return True


class TestDetermineHeaderPosition():

    @pytest.fixture(scope="module", params=[i for i in range(20)])
    def headers(self, request, table_headers):
        yield table_headers[request.param]

    def test_returns_list_of_tuples(self, table_headers) -> None:
        result = determine_header_positions(table_headers[0])
        assert isinstance(result, list)
        for position in result:
            assert isinstance(position, tuple)

    def test_returns_correct_header_positions(self, headers) -> None:
        expected = [(72.525, 691.72, 539.73, 703.72)]
        actual = determine_header_positions(headers)
        assert listAlmostEqual(actual, expected, delta=15)

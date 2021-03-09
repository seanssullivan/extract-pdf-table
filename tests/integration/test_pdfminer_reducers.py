# tests/integration/test_pdfminer_reducers.py

# Third-Party Imports
import pytest

# Local Imports
from src.parser.reducers.design import reduce_fontnames
from src.parser.reducers.design import reduce_fontsizes
from src.parser.reducers.design import reduce_fontweights
from src.parser.reducers.design import reduce_typefaces


class TestReduceFontNames():

    # @pytest.fixture(scope="function", params=[i for i in range(5)])
    # def font(self, request, fonts):
    #     yield fonts[request.param]

    def test_returns_list_of_strings_when_accumulator_is_a_list(self, fonts) -> None:
        result = reduce_fontnames([], fonts)
        assert isinstance(result, list)
        for fontname in result:
            assert isinstance(fontname, str)

    def test_returns_correct_fontname_when_only_one(self, fonts) -> None:
        actual = reduce_fontnames(set(), fonts[0])
        expected = set(['ArialMT'])
        assert actual == expected

    def test_returns_correct_fontnames_when_multiple(self, fonts) -> None:
        actual = reduce_fontnames(set(), fonts)
        expected = set(['ArialMT', 'Calibri-Bold', 'Georgia-Italic'])
        assert actual == expected


class TestReduceFontSizes():

    def test_returns_list_of_floats_when_accumulator_is_a_list(self, fonts) -> None:
        result = reduce_fontsizes([], fonts)
        assert isinstance(result, list)
        for fontsize in result:
            assert isinstance(fontsize, float)

    def test_returns_correct_fontsize_when_only_one(self, fonts) -> None:
        actual = reduce_fontsizes(set(), fonts[0])
        expected = set([8.0])
        assert actual == expected

    def test_returns_correct_fontsizes_when_multiple(self, fonts) -> None:
        actual = reduce_fontsizes(set(), fonts)
        expected = set([8.0, 9.0, 10.0])
        assert actual == expected


class TestReduceFontWeights():

    def test_returns_list_of_strings_when_accumulator_is_a_list(self, fonts) -> None:
        result = reduce_fontweights([], fonts)
        assert isinstance(result, list)
        for fontweight in result:
            assert isinstance(fontweight, str)

    def test_returns_correct_fontweight_when_only_one(self, fonts) -> None:
        actual = reduce_fontweights(set(), fonts[0])
        expected = set(['Regular'])
        assert not actual.difference(expected)

    def test_returns_correct_fontweights_when_multiple(self, fonts) -> None:
        actual = reduce_fontweights(set(), fonts)
        expected = set(['Regular', 'Bold', 'Italic'])
        assert not actual.difference(expected)


class TestReduceTypefaces():

    def test_returns_list_of_strings_when_accumulator_is_a_list(self, fonts) -> None:
        result = reduce_typefaces([], fonts)
        assert isinstance(result, list)
        for typeface in result:
            assert isinstance(typeface, str)

    def test_returns_correct_typeface_when_only_one(self, fonts) -> None:
        actual = reduce_typefaces(set(), fonts[0])
        expected = set(['ArialMT'])
        assert not actual.difference(expected)

    def test_returns_correct_typeface_when_multiple(self, fonts) -> None:
        actual = reduce_typefaces(set(), fonts)
        expected = set(['ArialMT', 'Calibri', 'Georgia'])
        assert not actual.difference(expected)

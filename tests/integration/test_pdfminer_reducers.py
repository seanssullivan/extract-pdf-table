# tests/integration/test_pdfminer_reducers.py

# Third-Party Imports
import pytest

# Local Imports
from parser.pdfminer.reducers.typography import reduce_fontnames
from parser.pdfminer.reducers.typography import reduce_fontsizes
from parser.pdfminer.reducers.typography import reduce_fontweights
from parser.pdfminer.reducers.typography import reduce_typefaces


class TestReduceFontNames():

    @pytest.fixture(autouse=True)
    def text(self, paragraphs):
        return paragraphs[0]

    def test_returns_list_of_strings_when_accumulator_is_a_list(self, text) -> None:
        result = reduce_fontnames([], text)
        assert isinstance(result, list)
        for fontname in result:
            assert isinstance(fontname, str)

    def test_returns_correct_fontname_when_only_one(self, text) -> None:
        actual = reduce_fontnames(set(), text)
        expected = set(['ArialMT'])
        assert actual == expected

    def test_returns_correct_fontnames_when_multiple(self, paragraphs) -> None:
        actual = reduce_fontnames(set(), paragraphs)
        expected = set(['ArialMT', 'Calibri-Italic', 'TimesNewRomanPS-BoldMT', 'Calibri-Italic'])
        assert actual == expected
    

class TestReduceFontSizes():

    @pytest.fixture(autouse=True)
    def text(self, paragraphs):
        return paragraphs[0]

    def test_returns_list_of_floats_when_accumulator_is_a_list(self, text) -> None:
        result = reduce_fontsizes([], text)
        assert isinstance(result, list)
        for fontsize in result:
            assert isinstance(fontsize, float)
    
    def test_returns_correct_fontsize_when_only_one(self, text) -> None:
        actual = reduce_fontsizes(set(), text)
        expected = set([18.0])
        assert actual == expected

    def test_returns_correct_fontsizes_when_multiple(self, paragraphs) -> None:
        actual = reduce_fontsizes(set(), paragraphs)
        expected = set([18.0, 14.0, 12.0])
        assert actual == expected


class TestReduceFontWeights():

    @pytest.fixture(autouse=True)
    def text(self, paragraphs):
        return paragraphs[0]

    def test_returns_list_of_strings_when_accumulator_is_a_list(self, text) -> None:
        result = reduce_fontweights([], text)
        assert isinstance(result, list)
        for fontweight in result:
            assert isinstance(fontweight, str)
    
    def test_returns_correct_fontweight_when_only_one(self, text) -> None:
        actual = reduce_fontweights(set(), text)
        expected = set(['Regular'])
        assert not actual.difference(expected)

    def test_returns_correct_fontweights_when_multiple(self, paragraphs) -> None:
        actual = reduce_fontweights(set(), paragraphs)
        expected = set(['BoldMT', 'Regular', 'Italic'])
        assert not actual.difference(expected)


class TestReduceTypefaces():

    @pytest.fixture(autouse=True)
    def text(self, paragraphs):
        return paragraphs[0]

    def test_returns_list_of_strings_when_accumulator_is_a_list(self, text) -> None:
        result = reduce_typefaces([], text)
        assert isinstance(result, list)
        for typeface in result:
            assert isinstance(typeface, str)

    def test_returns_correct_typeface_when_only_one(self, text) -> None:
        actual = reduce_typefaces(set(), text)
        expected = set(['ArialMT'])
        assert not actual.difference(expected)

    def test_returns_correct_typeface_when_multiple(self, paragraphs) -> None:
        actual = reduce_typefaces(set(), paragraphs)
        expected = set(['ArialMT', 'Calibri', 'TimesNewRomanPS', 'Calibri'])
        assert not actual.difference(expected)

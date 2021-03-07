# parser/pdfminer/utils/typography.py

# Standard Imports
import statistics

# Third-Party Imports
from pdfminer.layout import LTItem

# Local Imports
from ..reducers.design import reduce_fontnames
from ..reducers.design import reduce_fontsizes
from ..reducers.design import reduce_fontweights
from ..reducers.design import reduce_typefaces


def most_common_fontname(container: LTItem):
    """Return the most common fontname in the provided container."""
    return statistics.mode(reduce_fontnames([], container))


def most_common_fontsize(container: LTItem):
    """Return the most common fontsize in the provided container."""
    return statistics.mode(reduce_fontsizes([], container))


def most_common_fontweight(container: LTItem):
    """Return the most common fontweight in the provided container."""
    return statistics.mode(reduce_fontweights([], container))


def most_common_typeface(container: LTItem):
    """Return the most common typeface in the provided container."""
    return statistics.mode(reduce_typefaces([], container))

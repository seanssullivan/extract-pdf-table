import os
import math
from tqdm import tqdm

import numpy as np
import pandas as pd
from pdfminer.layout import LAParams

from helpers.abstractors import simplify
from helpers.selectors import extract_pages, extract_characters
from layout.positions import determine_line_positions, assign_characters_to_lines


def main():
    with open('tests/samples/sample_3.pdf', 'rb') as file:
        pages = extract_pages(file)
        table = extract_table(list(pages)[0])

        # for char in table:
        #     print(char)


def extract_table(page):
    chars = simplify(extract_characters(page))
    positions = determine_line_positions(chars)
    print(positions)
    # lines = assign_characters_to_lines(chars)

    table = pd.DataFrame()
    return table


if __name__ == "__main__":
    main()

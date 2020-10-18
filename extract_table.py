import os
from statistics import mean
from tqdm import tqdm

import numpy as np
import pandas as pd
from pdfminer.layout import LAParams

from helpers.abstractors import simplify
from helpers.consolidators import merge_by_proximity
from helpers.extractors import extract_pages, extract_characters
from layout.positions import assign_characters_to_lines, determine_column_positions


def main():
    with open('tests/samples/sample_3.pdf', 'rb') as file:
        pages = extract_pages(file)
        table = extract_table(list(pages)[0])

        # for char in table:
        #     print(char)


def extract_table(page):
    chars = simplify(extract_characters(page))

    margin = mean(map(lambda char: char['size'], chars))
    assigned_chars = assign_characters_to_lines(chars)

    merged_chars = merge_by_proximity(assigned_chars, margin, axis=1)
    col_positions = determine_column_positions(merged_chars)

    table = pd.DataFrame()
    return table


if __name__ == "__main__":
    main()

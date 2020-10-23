# extract_table.py

# Standard Imports
from statistics import mean

# Third-Party Imports
import pandas as pd

# Local Imports
from helpers.abstractors import simplify, summarize
from helpers.consolidators import merge_by_proximity
from helpers.extractors import extract_pages, extract_characters
from layout.positions import assign_characters_to_lines, assign_text_to_columns


def main():
    with open('tests/samples/sample_5.pdf', 'rb') as file:
        pages = extract_pages(file)
        for page in pages:
            table = extract_table(page)
            print(table)

        # for char in table:
        #     print(char)


def extract_table(page):
    chars = simplify(extract_characters(page))

    # Make sure we found characters on the page
    stats = summarize(chars)
    if stats['text'] == '':
        return None

    margin = mean(map(lambda char: char['size'], chars))
    lines = assign_characters_to_lines(chars)
    blocks = merge_by_proximity(lines, margin, axis=1)
    cells = assign_text_to_columns(blocks)

    # Get number of columns and rows in table
    first_row = min(map(lambda c: c['line_num'], cells))
    num_rows = max(map(lambda c: c['line_num'], cells)) + 1
    num_cols = max(map(lambda c: c['col_num'], cells)) + 1

    data = []
    headers = list(map(lambda c: c['text'].strip(), (filter(lambda c: c['line_num'] == first_row, cells))))
    for row in range(first_row + 1, num_rows):
        entry = {}
        properties = sorted(filter(lambda c: c['line_num'] == row, cells), key=lambda c: c['col_num'])
        for col in range(num_cols):
            entry[headers[col]] = properties[col]['text'].strip()
        
        data.append(entry)
            
    table = pd.DataFrame(data, columns=headers)
    return table


if __name__ == "__main__":
    main()

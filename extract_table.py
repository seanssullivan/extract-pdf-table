from io import BytesIO
import os
import math
import tempfile
from tqdm import tqdm

import numpy as np
from pdf2image import convert_from_bytes
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams
import pytesseract
from pytesseract import Output

from helpers.dimensions import average_height, average_width
from helpers.layout import sort_characters_into_rows, sort_characters_into_columns
from helpers.representation import simplify_characters
from helpers.selectors import extract_characters_from_page


def extract_table(filepath, page_range=None, output='text', use_ocr=False):
    return use_pytesseract(filepath, page_range, output) if use_ocr \
        else use_pdfminer(filepath, page_range, output)


def use_pytesseract(filepath, page_range=None, output='text'):
  with tempfile.TemporaryDirectory() as temp_dir:
    print(f"Extracting images from {os.path.basename(filepath)}...")
    image_paths = convert_pdf_to_images(filepath, temp_dir, page_range)

    print(f"Performing OCR on {len(image_paths)} images...")
    if output == 'text':
      result = pytesseract_characters(image_paths)
    elif output == 'data':
      result = pytesseract_data(image_paths)
    else:
      raise ValueError
  
  return result


def pytesseract_characters(paths):
  pdfs = [pytesseract.image_to_pdf_or_hocr(path, extension='pdf') for path in tqdm(paths)]

  pages = []
  for pdf in pdfs:
    pages.extend([page for page in extract_pages(BytesIO(pdf))])
  
  characters = []
  for page in tqdm(list(pages)):
    characters.extend(extract_table_from_page(page))
  
  return characters


def pytesseract_data(paths):
  characters = [pytesseract.image_to_data(path, output_type=Output.DICT) for path in tqdm(paths)]
  return characters


def use_pdfminer(filepath, page_range=None, output='text'):
  page_numbers = [n for n in range(page_range[0] - 1, page_range[-1])] if page_range else None

  params = LAParams(char_margin=100.0, detect_vertical=False)

  print(f"Extracting pages from {os.path.basename(filepath)}...")
  pages = extract_pages(filepath, page_numbers=page_numbers, laparams=params)

  print(f"Extracting table from page(s)...")
  characters = []
  for page in tqdm(list(pages)):
    characters.extend(extract_table_from_page(page))
  
  return characters


def convert_pdf_to_images(filepath, dir, page_range=None):
  if page_range:
    start, end = page_range[0], page_range[-1]
  else:
    start = end = None

  with open(filepath, 'rb') as pdf:
    print(f"Converting {os.path.basename(filepath)} into images...")
    image_paths = convert_from_bytes(
      pdf.read(), output_folder=dir, first_page=start, last_page=end, paths_only=True
    )
  return image_paths


def extract_table_from_page(page):
  characters = extract_characters_from_page(page)
  chars = simplify_characters(characters)
  table = format_table(chars)
  return table


def format_table(chars):
  # intersects = calculate_intersects(chars)
  # print(intersects.any(axis=1))
  # print(intersects.any(axis=0))

  y_margin = math.ceil(average_height(chars) / 2)
  rows = sort_characters_into_rows(chars, y_margin)

  x_margin = math.ceil(average_width(chars) / 2)
  table = sort_characters_into_columns(rows, x_margin)
  return table


def calculate_intersects(chars):
  max_top = math.floor(max(list(map(lambda char: char['top'], chars))))
  max_right = math.floor(max(list(map(lambda char: char['right'], chars))))
  min_bottom = math.floor(min(list(map(lambda char: char['bottom'], chars))))
  min_left = math.ceil(min(list(map(lambda char: char['left'], chars))))

  y_intersects = []
  for pos in range(max_top, min_bottom, -1):
    intersect = len(list(filter(lambda char: char['bottom'] < pos and char['top'] > pos, chars)))
    y_intersects.append(intersect)
  y_matrix = np.matrix(y_intersects).transpose()

  x_intersects = []
  for pos in range(min_left, max_right):
    intersect = len(list(filter(lambda char: char['left'] < pos / 10 and char['right'] > pos / 10, chars)))
    x_intersects.append(intersect)
  x_matrix = np.matrix(x_intersects)

  grid = np.dot(y_matrix, x_matrix)
  return grid

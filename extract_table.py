from io import BytesIO
import os
import math
import tempfile
from tqdm import tqdm

from pdf2image import convert_from_bytes
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams
import pytesseract

from helpers.dimensions import average_height, average_width
from helpers.layout import sort_characters_into_rows, sort_characters_into_columns
from helpers.representation import simplify_characters
from helpers.selectors import extract_characters_from_page


def extract_table(filepath, page_range, use_tesseract=False):
  start, end = page_range[0], page_range[-1]
  pages_numbers = f"page {end}" if start + 1 == end else f"pages {start + 1} to {end}"

  characters = []
  if not use_tesseract:
    params = LAParams(char_margin=100.0, detect_vertical=False)
    print(f"Extracting {pages_numbers} from {os.path.basename(filepath)}...")
    pages = extract_pages(filepath, page_numbers=[n for n in range(start, end)], laparams=params)
    
  else:
    with tempfile.TemporaryDirectory() as temp_dir:
      print(f"Extracting images from {os.path.basename(filepath)}...")
      image_paths = convert_pdf_to_images(filepath, temp_dir, start, end)

      print(f"Performing OCR on {len(image_paths)} images...")
      pdfs = [get_pdf_from_image(path) for path in tqdm(image_paths)]
      pages = []
      for pdf in pdfs:
        pages.extend([page for page in extract_pages(BytesIO(pdf))])
  
  print(f"Extracting table from page{'s' if end - start > 1 else ''}...")
  for page in tqdm(list(pages)):
    characters.extend(extract_table_from_page(page))
  
  return characters


def convert_pdf_to_images(filepath, dir, start, end):
  with open(filepath, 'rb') as pdf:
    print(f"Converting {os.path.basename(filepath)} into images...")
    image_paths = convert_from_bytes(
      pdf.read(), output_folder=dir, first_page=start, last_page=end, paths_only=True
    )
  return image_paths


def get_pdf_from_image(filepath):
  return pytesseract.image_to_pdf_or_hocr(filepath, extension='pdf')


def extract_table_from_page(page):
  characters = extract_characters_from_page(page)
  chars = simplify_characters(characters)
  table = format_table(chars)
  return table


def format_table(chars):
  y_margin = math.ceil(average_height(chars) / 2)
  rows = sort_characters_into_rows(chars, y_margin)

  x_margin = math.ceil(average_width(chars) / 2)
  table = sort_characters_into_columns(rows, x_margin)
  return table

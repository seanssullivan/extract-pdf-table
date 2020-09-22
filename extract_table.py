from io import BytesIO
import math
import tempfile
from tqdm import tqdm

from pdf2image import convert_from_path
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LAParams
import pytesseract

from helpers.dimensions import average_height, average_width
from helpers.layout import sort_characters_into_rows, sort_characters_into_columns
from helpers.representation import simplify_characters
from helpers.selectors import extract_characters_from_page


def extract_table(file_name, start, end):
  characters = []
  with tempfile.TemporaryDirectory() as temp_dir:
    images_from_path = convert_from_path(file_name, output_folder=temp_dir, first_page=start, last_page=end, paths_only=True)
    
    for image_path in tqdm(images_from_path):
      pdf_page = pytesseract.image_to_pdf_or_hocr(image_path, extension='pdf')
      table = extract_table_from_page(BytesIO(pdf_page))
      characters += table
  return characters


def extract_table_from_page(pdf_page):
  params = LAParams(char_margin=100.0, detect_vertical=False)
  pages = extract_pages(pdf_page, laparams=params)
  characters = [extract_characters_from_page(page) for page in pages][0]
  chars = simplify_characters(characters)

  y_margin = math.ceil(average_height(chars) / 2)
  rows = sort_characters_into_rows(chars, y_margin)

  x_margin = math.ceil(average_width(chars) / 2)
  table = sort_characters_into_columns(rows, x_margin)

  return table
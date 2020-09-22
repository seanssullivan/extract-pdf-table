from pdfminer.layout import LTTextContainer, LTChar

def extract_elements_from_page(pdf_page):
  return [element for element in pdf_page if isinstance(element, LTTextContainer)]


def extract_lines_from_element(pdf_element):
  return [line for line in pdf_element if isinstance(line, LTTextContainer)]


def extract_characters_from_line(pdf_line):
  return [character for character in pdf_line if isinstance(character, LTChar)]


def extract_elements_from_pages(pdf_pages):
  elements = []
  for pdf_page in pdf_pages:
    elements += extract_elements_from_page(pdf_page)
  return elements


def extract_lines_from_elements(pdf_elements):
  lines = []
  for pdf_element in pdf_elements:
    lines += extract_lines_from_element(pdf_element)
  return lines


def extract_characters_from_lines(pdf_lines):
  characters = []
  for pdf_line in pdf_lines:
    characters += extract_characters_from_line(pdf_line)
  return characters
  

def extract_lines_from_page(pdf_page):
  elements = extract_elements_from_page(pdf_page)
  lines = extract_lines_from_elements(elements)
  return lines


def extract_characters_from_element(pdf_element):
  lines = extract_lines_from_element(pdf_element)
  characters = extract_characters_from_lines(lines)
  return characters


def extract_characters_from_page(pdf_page):
  lines = extract_lines_from_page(pdf_page)
  characters = extract_characters_from_lines(lines)
  return characters


def extract_lines_from_pages(pdf_pages):
  text_pages = []
  for pdf_page in pdf_pages:
    lines = extract_lines_from_page(pdf_page)
    text_pages.append(lines)
  return text_pages


def extract_characters_from_elements(pdf_elements):
  text_elements = []
  for pdf_element in pdf_elements:
    characters = extract_characters_from_element(pdf_element)
    text_elements.append(characters)
  return text_elements


def extract_characters_from_pages(pages):
  characters = map(lambda page: extract_characters_from_page(page), pages)
  return list(characters)

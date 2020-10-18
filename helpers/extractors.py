# helpers/extractors.py

# Standard Imports
from io import StringIO
from typing import Generator

# Third-Party Imports
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTPage, LTTextContainer, LTTextBoxHorizontal, LTTextLineHorizontal, LTChar, LTAnno
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def extract_text(file):
    """Extract text from a PDF document using pdfminer.six.
    
    While we could just use pdfminer.high_level.extract_text(),
    the more verbose solution provides the opportunity to
    customize and extend the process later."""

    parser = PDFParser(file)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()

    with StringIO() as output:
        device = TextConverter(rsrcmgr, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)

        return output.getvalue()


def extract_pages(file):
    """Extract pages from a PDF document using pdfminer.six.
    
    While we could just use pdfminer.high_level.extract_pages(),
    the more verbose solution provides the opportunity to
    customize and extend the process later."""

    parser = PDFParser(file)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        yield layout


def extract_textboxes(element):
    """Function to select instances of LTTextBoxHorizontal inside LTPage objects."""

    # ensure argument is an LTPage object, then yield textboxes
    if isinstance(element, LTPage):
        for textbox in element:
            if isinstance(textbox, LTTextBoxHorizontal):
                yield textbox

    # check whether the object is a generator which might yield pages
    elif isinstance(element, Generator):
        for page in element:
            yield from extract_textboxes(page)

    # otherwise it is not an appropriate object type
    else:
        raise TypeError


def extract_lines(element):
    """Function to select instances of LTTextLineHorizontal inside LTTextBoxHorizontal objects."""

    # ensure argument is an LTTextBoxHorizontal object, then yield lines of text
    if isinstance(element, LTTextBoxHorizontal):
        for line in element:
            if isinstance(line, LTTextLineHorizontal):
                yield line

    # check whether the object is a generator which might yield textboxes
    elif isinstance(element, Generator):
        for obj in element:
            yield from extract_lines(obj)

    # for LTPage objects, retrieve the textboxes first
    elif type(element) in [LTPage]:
        for textbox in extract_textboxes(element):
            yield from extract_lines(textbox)

    # otherwise it is not an appropriate object type
    else:
        raise TypeError


def extract_characters(element):
    """Function to select instances of LTChar inside LTTextLineHorizontal objects."""
    
    # ensure parameter is an LTTextLineHorizontal object, then yield characters
    if isinstance(element, LTTextLineHorizontal):
        for char in element:
            if isinstance(char, LTChar):
                yield char

    # check whether the object is a generator which might yield lines of text
    elif isinstance(element, Generator):
        for obj in element:
            yield from extract_characters(obj)

    # for LTPage or LTTextBoxHorizontal objects, retrieve the lines of text first
    elif type(element) in [LTTextBoxHorizontal, LTPage]:
        for line in extract_lines(element):
            yield from extract_characters(line)

    # otherwise it is not an appropriate object type
    else:
        raise TypeError

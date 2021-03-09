# src/parser/extractors/pages.py

# Standard Imports
from typing import BinaryIO, Iterator, Text, Union

# Third-Party Imports
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def extract_pages(file: Union[BinaryIO, Text], **params) -> Iterator[LTPage]:
    """Extract pages from a PDF document using pdfminer.six.

    While we could just use pdfminer.high_level.extract_pages(),
    the more verbose solution provides the opportunity to
    customize and extend the process later."""

    # Initialize parser, document and resource manager
    parser = PDFParser(file)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()

    # Initialize layout analysis parameters
    laparams = LAParams(**params) if params else LAParams()

    # Initialize page aggregator and interpreter
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Process page layouts
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        yield layout

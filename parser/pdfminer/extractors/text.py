# parser/pdfminer/extractors/text.py

# Standard Imports
from io import StringIO
from typing import BinaryIO, Text, Union

# Third-Party Imports
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def extract_text(file: Union[BinaryIO, Text], **params) -> str:
    """Extract text from a PDF document using pdfminer.six.
    
    While we could just use pdfminer.high_level.extract_text(),
    the more verbose solution provides the opportunity to
    customize and extend the process later."""

    # Initialize parser, document and resource manager
    parser = PDFParser(file)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()

    # Initialize layout analysis parameters
    laparams = LAParams(**params) if params else LAParams()

    with StringIO() as output:
        # Initialize page aggregator and interpreter
        device = TextConverter(rsrcmgr, output, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Process page text
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)

        return output.getvalue()

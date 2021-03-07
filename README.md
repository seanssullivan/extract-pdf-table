# extract-pdf-table

A wrapper for pdfminer.six which extracts tabulated data from PDF files. It uses layout analysis to detect and isolate tables, and uses the relative distance between text lines to determine the width of each column in order to more accurately extract text from cells.

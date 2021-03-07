# src/pdfminer/abstractors/font.py

# Standard Imports
from typing import Text

# Third-Party Imports
from pdfminer.layout import LTChar


def get_fontname(character: LTChar) -> Text:
    return (
        character.fontname.split('+')[1]
        if '+' in character.fontname
        else character.fontname
    )


def get_fontsize(character: LTChar) -> int:
    return character.size


def get_fontweight(character: LTChar) -> Text:
    font = get_fontname(character)
    return (
        font.split('-')[1]
        if '-' in font
        else 'Regular'
    )


def get_typeface(character: LTChar) -> Text:
    font = get_fontname(character)
    return (
        font.split('-')[0]
        if '-' in font
        else font
    )

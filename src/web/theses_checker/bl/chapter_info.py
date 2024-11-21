#----------------------------------------------------------------------------
# File          : theses_checker.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Created Date  : 20.11.2024
# Last Updated  : 20.11.2024
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

from math import pi
from typing import NamedTuple


class Pages(NamedTuple):
    """
    Information about the pages of a chapter.

    Attributes:
        first (int): Number of the first page of the chapter. Page indexing starts from 1.
        last (int): Number of the last page of the chapter. Page indexing starts from 1.
    """
    first: int ## Number of the first page of the chapter. Page indexing starts from 1.
    last: int ## Number of the last page of the chapter. Page indexing starts from 1.

class TextInfo(NamedTuple):
    """
    Information about the text in a chapter.

    Attributes:
        totalCharCount (int): Total character count.
        nonWhiteCharCount (int): Total character count without white characters.
        totalWordCount (int): Total word count.
    """
    totalCharCount: int ## Total character count.
    nonWhiteCharCount: int ## Total character count without white characters.
    totalWordCount: int ## Total word count.

class PictureInfo(NamedTuple):
    """
    Information about a picture in a chapter.

    Attributes:
        bbox (tuple): Bounding box of the picture. Tuple of 4 integers: (x0, y0, x1, y1).
        page (int): Number of the page where the picture is located. Page indexing starts from 1.
    """
    bbox: tuple ## Bounding box of the picture. Tuple of 4 integers: (x0, y0, x1, y1).
    page: int ## Number of the page where the picture is located. Page indexing starts from 1.

class ChapterInfo:
    """
    Information about a chapter in a document.

    Attributes:
        sequence (int): Sequence number of the chapter. Starting from 1.
        title (str): Title of the chapter.
        pages (Pages): Pages of the chapter.
        textInfo (TextInfo): Information about the text in the chapter.
        pictures (list): List of PictureInfo objects.
    """

    def __init__(self, sequence: int = 0, title: str = None, pages: Pages = Pages(0, 0), textInfo: TextInfo = TextInfo(0, 0, 0), pictures: list = []):
        """
        Constructor.

        Args:
            sequence (int): Sequence number of the chapter. Starting from 1.
            title (str): Title of the chapter.
            pages (Pages): Pages of the chapter.
            textInfo (TextInfo): Information about the text in the chapter.
            pictures (list): List of PictureInfo objects.
        """
        self.sequence : int = sequence 
        self.title : str = title
        self.pages : Pages = pages
        self.textInfo : TextInfo = textInfo
        self.pictures : list = pictures
    
    def addPicture(self, bbox: tuple, page: int):
        """
        Adds a picture to the chapter.

        Args:
            bbox (tuple): Bounding box of the picture. Tuple of 4 integers: (x0, y0, x1, y1).
            page (int): Number of the page where the picture is located. Page indexing starts from 1.
        """
        self.pictures.append(PictureInfo(bbox, page))

    def addText(self, text: str):
        """
        Adds text to the text information of the chapter.

        Args:
            text (str): Text to add.
        """
        self.textInfo = TextInfo(
            totalCharCount= self.textInfo.totalCharCount + len(text),
            nonWhiteCharCount= self.textInfo.nonWhiteCharCount + len(text.replace(" ", "").replace("\n", "")),
            totalWordCount= self.textInfo.totalWordCount + len(text.split())
        )

    def addPage(self, page: int):
        """
        Adds a page to the chapter.

        Args:
            page (int): Page number to add.
        """
        if self.pages.first == 0:
            self.pages = Pages(page, page)
        else:
            self.pages = Pages(self.pages.first, page)
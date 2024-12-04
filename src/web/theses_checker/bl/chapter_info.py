#----------------------------------------------------------------------------
# File          : chapter_info.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Created Date  : 20.11.2024
# Last Updated  : 25.11.2024
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

from math import pi
from typing import NamedTuple


class Pages:
    """
    Information about the pages of a chapter.

    Attributes:
        first (int): Number of the first page of the chapter. Page indexing starts from 1.
        last (int): Number of the last page of the chapter. Page indexing starts from 1.
    """
    first: int ## Number of the first page of the chapter. Page indexing starts from 1.
    last: int ## Number of the last page of the chapter. Page indexing starts from 1.

    def __init__(self, first: int = 0, last: int = 0):
        """
        Constructor.

        Args:
            first (int): Number of the first page of the chapter. Page indexing starts from 1.
            last (int): Number of the last page of the chapter. Page indexing starts from 1.
        """
        self.first = first
        self.last = last

    def toDict(self):
        """
        Converts the object to a dictionary.

        Returns:
            dict: Dictionary with the attributes of the object.
        """
        return {
            "first": self.first,
            "last": self.last,
            "count": self.count()
        }
    
    def count(self):
        """
        Counts the number of pages in the chapter.

        Returns:
            int: Number of pages in the chapter.
        """
        return self.last - self.first + 1

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
        pictures (list): List of objects with information about pictures in the chapter.
    """

    def __init__(self, sequence: int = 0, title: str|None = None, pages: Pages|None = None, textInfo: TextInfo|None = None, pictures: list[PictureInfo]|None = None):
        """
        Constructor.

        Args:
            sequence (int): Sequence number of the chapter. Starting from 1.
            title (str|None, optional): Title of the chapter.
            pages (Pages|None, optional): Pages of the chapter.
            textInfo (TextInfo|None, optional): Information about the text in the chapter.
            pictures (list[PictureInfo]|None, optional): List of objects with information about pictures in the chapter.
        """
        self.sequence : int = sequence 
        self.title : str = title
        self.pages : Pages = pages if pages is not None else Pages(0, 0)
        self.textInfo : TextInfo = textInfo if textInfo is not None else TextInfo(0, 0, 0)
        self.pictures : list[PictureInfo] = pictures if pictures is not None else []
    
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
        Adds information on 'text' to the text information of the chapter.

        Args:
            text (str): Text to analyze and add its information to the text information of the chapter.
        """
        text_split = text.split()
        self.textInfo = TextInfo(
            totalCharCount= self.textInfo.totalCharCount + len(text),
            nonWhiteCharCount= self.textInfo.nonWhiteCharCount + len("".join(text_split)),
            totalWordCount= self.textInfo.totalWordCount + len(text_split)
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
            self.pages.last = page
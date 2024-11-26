#----------------------------------------------------------------------------
# File          : chapter_standard_page_info.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Created Date  : 26.11.2024
# Last Updated  : 26.11.2024
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

from typing import NamedTuple
from .chapter_info import *
from .standard_pages import *

class PictureInfoAdvanced:
    """
    Advanced information about a picture in a chapter.

    Attributes:
        bbox (tuple[float, float, float, float]): Bounding box of the picture. Tuple of 4 floats: (x0, y0, x1, y1).
        page (int): Number of the page where the picture is located. Page indexing starts from 1.
        area (float): Image area in cm^2. Rounded to 2 decimal places.
        stdPages (float): Image area converted to standard pages. Rounded to 2 decimal places.
        charCount (int): Number of characters corresponding to the image standard pages.
    """
    bbox: tuple[float, float, float, float] ## Bounding box of the picture. Tuple of 4 floats: (x0, y0, x1, y1).
    page: int ## Number of the page where the picture is located. Page indexing starts from 1.
    area: float ## Image area in cm^2. Rounded to 2 decimal places.
    stdPages: float ## Image area converted to standard pages. Rounded to 2 decimal places.
    charCount: int ## Number of characters corresponding to the image standard pages.

    def __init__(self, pictureInfo : PictureInfo):
        """
        Initialize the PictureInfoAdvanced object from the PictureInfo object.

        Args:
            pictureInfo (PictureInfo): PictureInfo object.
        """
        area = self.__countArea(pictureInfo.bbox)

        self.bbox : tuple[float, float, float, float] = pictureInfo.bbox
        self.page : int = pictureInfo.page
        self.area : float = round(area, 2)
        self.stdPages = countStandardPagesFromImageArea(area)
        self.charCount = standardPagesToChars(self.stdPages)

    def __countArea(self, bbox : tuple[float, float, float, float]) -> float:
        """
        Count the area of the image in cm^2 from the bounding box.

        Args:
            bbox (tuple): Bounding box of the picture. Tuple of 4 floats: (x0, y0, x1, y1).
        """
        x0, y0, x1, y1 = bbox
        height_cm = pxToCm(abs(x1 - x0))
        width_cm = pxToCm(abs(y1 - y0))
        return height_cm * width_cm

class TextInfoAdvanced:
    """
    Advanced information about the text in a chapter.

    Attributes:
        totalCharCount (int): Total character count.
        totalCharCountStdPages (float): Total character count converted to standard pages. Rounded to 2 decimal places.
        nonWhiteCharCount (int): Total character count without white characters.
        nonWhiteCharCountStdPages (float): Total character count without white characters converted to standard pages. Rounded to 2 decimal places.
        totalWordCount (int): Total word count.
        totalWordCountStdPages (float): Total word count converted to standard pages. Rounded to 2 decimal places.
    """
    totalCharCount: int ## Total character count.
    totalCharCountStdPages: float ## Total character count converted to standard pages. Rounded to 2 decimal places.
    nonWhiteCharCount: int ## Total character count without white characters.
    nonWhiteCharCountStdPages: float ## Total character count without white characters converted to standard pages. Rounded to 2 decimal places.
    totalWordCount: int ## Total word count.

    def __init__(self, textInfo : TextInfo):
        """
        Initialize the TextInfoAdvanced object from the TextInfo object.

        Args:
            textInfo (TextInfo): TextInfo object.
        """
        self.totalCharCount : int = textInfo.totalCharCount
        self.totalCharCountStdPages : float = countStandardPagesFromChars(textInfo.totalCharCount)
        self.nonWhiteCharCount : int = textInfo.nonWhiteCharCount
        self.nonWhiteCharCountStdPages : float = countStandardPagesFromChars(textInfo.nonWhiteCharCount)
        self.totalWordCount : int = textInfo.totalWordCount

class ChapterInfoAdvanced:
    """
    Advanced information about a chapter in a document.

    Attributes:
        sequence (int): Sequence number of the chapter. Starting from 1.
        title (str): Title of the chapter.
        pages (Pages): Pages of the chapter.
        textInfo (TextInfoAdvanced): Information about the text in the chapter.
        pictures (list[PictureInfoAdvanced]): List of objects with advanced information about pictures in the chapter.
    """

    def __init__(self, chapterInfo : ChapterInfo):
        """
        Initialize the ChapterInfoAdvanced object from basic information about the chapter.

        Args:
            chapterInfo (ChapterInfo): Basic information about the chapter.
        """
        self.sequence : int = chapterInfo.sequence 
        self.title : str = chapterInfo.title
        self.pages : Pages = chapterInfo.pages
        self.textInfo : TextInfoAdvanced = TextInfoAdvanced(chapterInfo.textInfo)
        self.pictures : list[PictureInfoAdvanced] = [PictureInfoAdvanced(picture) for picture in chapterInfo.pictures]


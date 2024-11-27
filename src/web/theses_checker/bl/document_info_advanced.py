#----------------------------------------------------------------------------
# File          : chapter_standard_page_info.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Created Date  : 26.11.2024
# Last Updated  : 26.11.2024
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

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
        picturesStdPages (float): Total standard pages of the pictures in the chapter. Rounded to 2 decimal places.
        totalStdPages (float): Total standard pages of the chapter. Rounded to 2 decimal places.
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
        self.picturesStdPages : float = round(sum([picture.stdPages for picture in self.pictures]), 2)
        self.totalStdPages : float = round(self.textInfo.totalCharCountStdPages + self.picturesStdPages, 2)
    
    def toDict(self) -> dict:
        """
        Convert the ChapterInfoAdvanced object to a dictionary.

        Returns:
            dict: Dictionary with the chapter information.
        """
        return {
            'sequence': self.sequence,
            'title': self.title,
            'pages': self.pages.__dict__,
            'textInfo': self.textInfo.__dict__,
            'pictures': [picture.__dict__ for picture in self.pictures],
            'picturesStdPages': self.picturesStdPages,
            'totalStdPages': self.totalStdPages
        }

class DocumentInfoAdvanced:
    """
    Advanced information about a document.

    Attributes:
        chapters (list[ChapterInfoAdvanced]): List of objects with advanced information about chapters in the document.
        totalStdPages (float): Total standard pages of the document. Rounded to 2 decimal places.
    """
    chapters: list[ChapterInfoAdvanced] ## List of objects with advanced information about chapters in the document.
    totalStdPages: float ## Total standard pages of the document. Rounded to 2 decimal places.

    def __init__(self, chaptersInfo : list[ChapterInfo]):
        """
        Initialize the DocumentInfoAdvanced object from basic information about the chapters in the document.

        Args:
            chaptersInfo (list[ChapterInfo]): Basic information about the chapters in the document.
        """
        self.chapters : list[ChapterInfoAdvanced] = [ChapterInfoAdvanced(chapter) for chapter in chaptersInfo]
        self.totalStdPages : float = round(sum([chapter.totalStdPages for chapter in self.chapters]), 2)

    # def __init__(self, chaptersInfo : list[ChapterInfoAdvanced]):
    #     """
    #     Initialize the DocumentInfoAdvanced object from advanced information about the chapters in the document.

    #     Args:
    #         chaptersInfo (list[ChapterInfoAdvanced]): Advanced information about the chapters in the document.
    #     """
    #     self.chapters : list[ChapterInfoAdvanced] = chaptersInfo
    #     self.totalStdPages : float = round(sum([chapter.totalStdPages for chapter in self.chapters]), 2)

    def toDict(self) -> dict:
        """
        Convert the DocumentInfoAdvanced object to a dictionary.

        Returns:
            dict: Dictionary with the document information.
        """
        return {
            'chapters': [chapter.toDict() for chapter in self.chapters],
            'totalStdPages': self.totalStdPages
        }

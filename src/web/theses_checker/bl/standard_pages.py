#----------------------------------------------------------------------------
# File          : standard_pages.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Created Date  : 23.10.2024
# Last Updated  : 09.12.2024
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

PDF_STD_RESOLUTION = 72 ## standard resolution of PDF files in pixels per inch (72 pixels = 1 inch)
INCH_TO_CM = 2.54 ## 1 inch = 2.54 cm
CHARS_PER_STD_PAGE = 1800 ## average number of characters per standard page
IMAGE_AREA_TO_STD_PAGE = 180 ## conversion ratio from image area (cm^2) to standard pages (picture_area [cm^2] / IMAGE_AREA_TO_STD_PAGE [cm^2] = number_of_standard_pages); approx. 10 characters per cm^2

def pxToCm(px : int) -> float:
    """
    Convert pixels to centimeters.

    Args:
        px (int): Number of pixels.

    Returns:
        float: Number of centimeters.
    """
    return px * (INCH_TO_CM/PDF_STD_RESOLUTION)

def standardPagesToChars(stdPages : float) -> int:
    """
    Convert the number of standard pages to the corresponding number of characters.

    Args:
        stdPages (float): Number of standard pages.

    Returns:
        int: Corresponding number of characters.
    """
    return int(stdPages * CHARS_PER_STD_PAGE)

def countStandardPagesFromChars(charCount : int) -> float:
    """
    Count the number of standard pages from the character count.

    Args:
        charCount (int): Number of characters.

    Returns:
        float: Number of standard pages. Rounded to 2 decimal places.
    """
    return round(float(charCount)/CHARS_PER_STD_PAGE, 2)

def countStandardPagesFromImageBbox(bbox : tuple[float, float, float, float]) -> float:
    """
    Count the number of standard pages from the image bounding box.

    Args:
        bbox (tuple): Bounding box of the picture. Tuple of 4 floats: (x0, y0, x1, y1).

    Returns:
        float: Number of standard pages. Rounded to 2 decimal places.
    """
    height_cm = round(pxToCm(abs(bbox[2] - bbox[0])), 4)
    width_cm = round(pxToCm(abs(bbox[3] - bbox[1])), 4)
    return countStandardPagesFromImageArea(height_cm * width_cm)

def countStandardPagesFromImageArea(area : float) -> float:
    """
    Count the number of standard pages from the image area (cm^2).

    Args:
        area (float): Image area in cm^2.

    Returns:
        float: Number of standard pages. Rounded to 2 decimal places.
    """
    return round(area/IMAGE_AREA_TO_STD_PAGE, 2)


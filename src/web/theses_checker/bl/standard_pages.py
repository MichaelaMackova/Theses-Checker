#----------------------------------------------------------------------------
# File          : standard_pages.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 23.10.2024
# Last Updated  : 24.10.2024
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

def pxToCm(px:int):
    """
    TODO:
    """
    return px * (2.54/72) # using standard resolution 72 pixels = 1 inch (2.54 cm)

def countStandardPagesFromText(charCount:int):
    """
    TODO:
    """
    return round(charCount/1800.0, 2)

def countStandardPagesFromImage(bbox):
    """
    TODO:
    """
    height_cm = round(pxToCm(abs(bbox[2] - bbox[0])), 4)
    width_cm = round(pxToCm(abs(bbox[3] - bbox[1])), 4)
    return round((height_cm*width_cm)/(15.5 * 22.5), 2) #TODO: old ratio -> new ratio: cm2 / 350 + information about how many characters it makes
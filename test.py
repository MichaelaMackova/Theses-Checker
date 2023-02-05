from math import isclose
from statistics import median, mode
import fitz
import re


# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("C:\\Users\\micha\\Desktop\\Michaela\\Skola\\VS\\bakalarka\\pdf\\fit\\24779.pdf")
# -------------------------------------------------------------------------------------------


def __deleteDuplicate(array : list):
    return list(dict.fromkeys(array))


for page in doc:

    text_blocks = page.get_text("blocks", flags=fitz.TEXT_PRESERVE_LIGATURES|fitz.TEXT_DEHYPHENATE|fitz.TEXT_MEDIABOX_CLIP)

    for block in text_blocks:
        if block[6] != 0:
            print(block)
        text = block[4]
        if text[-1] == "\n":
            text = text[:-1]
        
        text = text.replace("\n"," ")
        x = re.findall("\S\(", text)    # " ("
        if x:
            print(__deleteDuplicate(x))
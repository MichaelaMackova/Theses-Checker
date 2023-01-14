#----------------------------------------------------------------------------
# File          : hyphen_test.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 28.10.2022
# ---------------------------------------------------------------------------

import string
import sys
import random
from statistics import median
import fitz



RND_PAGE_CNT = 10
RED = (204, 0, 0)
HIGH_RED = (255, 128, 128)

def rgb_to_pdf(color:tuple):
    return (color[0]/255.0, color[1]/255.0, color[2]/255.0)

def highlight(page:fitz.Page, rects:list, color:tuple, text:string):
    annot = page.add_highlight_annot(rects)
    annot.set_colors(stroke=rgb_to_pdf(color))

    info = annot.info
    if color == HIGH_RED:
        info["title"] = "Chyba"
    info["content"] = text

    annot.set_info(info)
    annot.update()




# ---------------------------------------------- MAIN --------------------------------------------------------
def annotate(origDocPath : string, annotatedDirPath : string):

    # if len(sys.argv) != 2 or sys.argv[1] == "-h":
    #     print("Description:")
    #     print("\tMakes a new pdf file called 'annotated.pdf' in the folder, where this program is saved.")
    #     print()
    #     print("Usage:\t\tpython .\\small_image_test.py <PDFfilePath>")
    #     print("For example:\tpython .\\small_image_test.py .\\pdf\\check.pdf")
    #     print()
    #     exit()


    doc = fitz.Document(origDocPath)

    for page in doc:
        rects = page.search_for(" - ")
        for rect in rects:
            highlight(page,rect,HIGH_RED,"Pouzijte spojovnik (–) namisto pomlcky.")
        # dictionary = page.get_text("dict")
        # blocks = dictionary['blocks']

        # for block in blocks:
        #     if block['type'] == 0: #text-block
        #         lines = block['lines']
        #         for line in lines:
        #             spans = line['spans']
        #             text = ""
        #             for span in spans:
        #                 text += span['text']
        #             # — –  – - 

        #             if " - " in text:
        #                 rects = page.search_for(" - ",clip=line['bbox'])
        #                 highlight(page,rects,HIGH_RED,"spojovník")



    
    # last = docPath.rfind('\\')
    # if last == -1:
    #     last = docPath.rfind('/')
    # replaceStr = docPath[(last+1):]
    # doc.save(docPath.replace(replaceStr, "annotated.pdf"))

    doc.save(annotatedDirPath + "annotated.pdf")
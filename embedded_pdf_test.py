import sys
import random
from statistics import median
import fitz

# ---------------------------------------------- MAIN --------------------------------------------------------

if len(sys.argv) != 2 or sys.argv[1] == "-h":
    print("Description:")
    print("\tMakes a new pdf file called 'annotated.pdf' in the folder, where this program is saved.")
    print()
    print("Usage:\t\tpython .\\small_image_test.py <PDFfilePath>")
    print("For example:\tpython .\\small_image_test.py .\\pdf\\check.pdf")
    print()
    exit()


doc = fitz.Document(sys.argv[1])

rect = doc.get_page_xobjects(0)[0][3]
print(rect)

doc[0].add_highlight_annot(rect)

doc.save("annotated.pdf")
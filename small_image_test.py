#----------------------------------------------------------------------------
# File          : small_image_test.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 28.10.2022
# ---------------------------------------------------------------------------

import sys
import random
from statistics import median
import fitz



RND_PAGE_CNT = 10
RED = (204, 0, 0)



def rgb_to_pdf(color:tuple):
    return (color[0]/255.0, color[1]/255.0, color[2]/255.0)

def random_pages_index(max_list_len:int, doc_len:int):
    if doc_len < max_list_len:
        max_list_len = doc_len
    return random.sample(range(0, doc_len), max_list_len)

def get_page_border(page:fitz.Page):
    potential_x0 = []
    potential_x1 = []
    
    dictionary = page.get_text("dict")
    blocks = dictionary['blocks']

    for block in blocks:

        if block['type'] == 0:
            lines = block['lines']

            if len(lines) > 1:
                origin_y = -1.0
                origin_x = -1.0

                for line in lines:
                    line_origin = line['spans'][0]['origin']

                    if line_origin[1] == origin_y:
                        # not a new line, just tab -> pop previous x1
                        potential_x1.pop()
                    else:
                        potential_x0.append(line['bbox'][0])

                        if line_origin[0] > origin_x and origin_x != -1.0:
                            # new paragraph
                            potential_x1.pop() #pop the last line in previous paragraph
                            potential_x0.pop() #pop this line -> indent

                        origin_x = line_origin[0]

                    origin_y = line_origin[1]
                    potential_x1.append(line['bbox'][2])

                potential_x1.pop() #pop the last line in paragraph

        else: #type = 1
            potential_x0.append(block['bbox'][0])
            potential_x1.append(block['bbox'][2])

    x0 = -1.0
    if potential_x0:
        x0 = median(potential_x0)

    x1 = -1.0
    if potential_x1:
        x1 = median(potential_x1)
    
    return (x0, x1)

def get_doc_border(doc:fitz.Document):
    right_borders = []
    left_borders = []
    rnd_page_i = random_pages_index(RND_PAGE_CNT,len(doc))

    for i in rnd_page_i:
        page = doc[i]
        x0, x1 = get_page_border(page)
        right_borders.append(x1)
        left_borders.append(x0)

    return (median(left_borders), median(right_borders))

def overflow_line(page:fitz.Page, x:float, overflow_rects:list):
    for rect in overflow_rects:
        annot = page.add_line_annot(fitz.Point(x,rect[1]), fitz.Point(x,rect[3]))
        annot.set_border(width=1)
        annot.set_colors(stroke=rgb_to_pdf(RED))
        annot.update()




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

border = get_doc_border(doc)
line_width = border[1] - border[0]


for page in doc:
    rects = []
    dictionary = page.get_text("dict")
    blocks = dictionary['blocks']

    for block in blocks:
        if block['type'] == 1:
            image_box = block['bbox']

            image_width = image_box[2] - image_box[0]
            percentage = (image_width * 100.0)/line_width
            

            if percentage > 85.0 and percentage < 99.0:
                print(percentage)
                rects.append(image_box)

    overflow_line(page,border[0],rects)
    overflow_line(page,border[1],rects)

doc.save("annotated.pdf")
print("\n--DONE--\n")


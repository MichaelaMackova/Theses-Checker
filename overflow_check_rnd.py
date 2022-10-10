#----------------------------------------------------------------------------
# File          : overflow_check.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 10.10.2022
# ---------------------------------------------------------------------------

import random
from statistics import median
import fitz

RND_PAGE_CNT = 10

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

def get_doc_border(doc):
    right_borders = []
    left_borders = []
    rnd_page_i = random_pages_index(RND_PAGE_CNT,len(doc))

    for i in rnd_page_i:
        page = doc[i]
        x0, x1 = get_page_border(page)
        right_borders.append(x1)
        left_borders.append(x0)

    return (median(left_borders), median(right_borders))


# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("C:\\Users\\micha\\Desktop\\Michaela\\Skola\\VS\\bakalarka\\pdf\\overflow.pdf")
# -------------------------------------------------------------------------------------------

border = get_doc_border(doc)
print(border)

page = doc[0]
pixmap = page.get_pixmap()

WHITE = (255, 255, 255)
overflow_rects = [None]

r_border = round(border[1])
y = 0
while y < pixmap.height:
    x = pixmap.width - 1
    while x > r_border:
        if pixmap.pixel(x,y) != WHITE:

            if overflow_rects[-1] == None:
                overflow_rects.pop()
                overflow_rects.append([r_border,y,x,y])
            else: 
                overflow_rects[-1][2] = max(overflow_rects[-1][2],x)
                overflow_rects[-1][3] = y
            break
        x = x - 1
    
    if x == r_border and overflow_rects[-1] != None:
        overflow_rects.append(None)
    y = y + 1
overflow_rects.pop()

print()
print(overflow_rects)


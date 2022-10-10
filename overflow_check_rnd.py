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


# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("C:\\Users\\micha\\Desktop\\Michaela\\Skola\\VS\\bakalarka\\pdf\\25073_overflow(page_51).pdf")
# -------------------------------------------------------------------------------------------

right_borders = []
left_borders = []

rnd_page_i = random_pages_index(RND_PAGE_CNT,len(doc))
print("pages:")
print(rnd_page_i)

for i in rnd_page_i:
    page = doc[i]
    x0, x1 = get_page_border(page)
    right_borders.append(x1)
    left_borders.append(x0)

print("left:")
print(median(left_borders))
print("right:")
print(median(right_borders))
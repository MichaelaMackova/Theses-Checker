#----------------------------------------------------------------------------
# File          : overflow_check.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 9.10.2022
# ---------------------------------------------------------------------------

from statistics import median
import fitz

# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("C:\\Users\\micha\\Desktop\\Michaela\\Skola\\VS\\bakalarka\\pdf\\25073_overflow(page_51).pdf")
# -------------------------------------------------------------------------------------------

right_borders = []

for page in doc:
    potential_x2 = []
    
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
                        # not a new line, just tab -> pop previous
                        potential_x2.pop()
                    else:

                        if line_origin[0] > origin_x and origin_x != -1.0:
                            # new paragraph
                            potential_x2.pop() #pop the last line in previous paragraph

                        origin_x = line_origin[0]

                    origin_y = line_origin[1]
                    potential_x2.append(line['bbox'][2])

                potential_x2.pop() #pop the last line in paragraph

        else: #type = 1
            potential_x2.append(block['bbox'][2])

    x2 = -1.0
    if potential_x2:
        x2 = median(potential_x2)
    right_borders.append(x2)

print(right_borders)
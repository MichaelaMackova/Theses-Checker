from math import isclose
from statistics import median, mode
import fitz



# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("C:\\Users\\micha\\Desktop\\Michaela\\Skola\\VS\\bakalarka\\pdf\\readme2.pdf")
# -------------------------------------------------------------------------------------------





#page = doc[0]

for page in doc:
    text_blocks = page.get_text("blocks")
    #print(text_blocks)
    potential_x2 = []

    for block in text_blocks:
        #pokud má více jak 1 '\n'
        block_text = block[4].split('\n')
        block_text.pop()
        print(block_text)
        line_count = len(block_text)
        #print(line_count)
        if line_count > 2:
            for line in block_text:
                block_rect = fitz.Rect(block[0],block[1],block[2],block[3])
                rects = page.search_for(line,clip=block_rect)
                #print(line)
                #print(rects)
                
                if len(rects) > 0:
                    rect = rects[-1]
                    #annot = page.add_highlight_annot([rect])
                    #annot.set_colors(stroke=(0.5, 1, 1))
                    #annot.update()
                    potential_x2.append(rect.x1)


    #print(potential_x2)
    if len(potential_x2) > 0:
        x2 = median(potential_x2)
        #print(x2)

        gold = (1, 0, 0)

        rect = fitz.Rect(x2, 0, x2, page.mediabox.y1)
        #print(rect.tl)
        #print(rect.bl)
        annot = page.add_line_annot(rect.tl, rect.bl)
        annot.set_border(width=1)
        annot.set_colors(stroke=gold)
        annot.update()

doc.save("annotated.pdf")
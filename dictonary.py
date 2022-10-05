import fitz

# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("C:\\Users\\micha\\Desktop\\Michaela\\Skola\\VS\\bakalarka\\pdf\\readme2.pdf")
# -------------------------------------------------------------------------------------------

page = doc[0]


# if origin y is the same => one line

dictionary = page.get_text("dict")
blocks = dictionary['blocks']
for block in blocks:
    lines = block['lines']
    for line in lines:
        print(line)
        print(line['bbox'])
        print()
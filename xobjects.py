import fitz

# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("C:\\Users\\micha\\Desktop\\Michaela\\Skola\\VS\\bakalarka\\pdf\\readme2.pdf")
# -------------------------------------------------------------------------------------------

page = doc[0]

xobjects = page.get_xobjects()

#print(xobjects)

for xref in range(1, doc.xref_length()):
    print(doc.xref_object(xref)) #string
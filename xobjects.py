import fitz
import sys

# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("doc1.pdf")
# -------------------------------------------------------------------------------------------

page = doc[0]

print(doc.xref_get_keys(1))

print(doc.xref_object(1))

print('\n--------------\n')

print(doc.xref_get_key(1,'Length'))

#print(doc.xref_stream_raw(1))


#xobjects = page.get_xobjects()

#print(page.transformation_matrix)
#print(xobjects)

# for xref in range(1, doc.xref_length()):
#     print(xref, '\n')
#     print(doc.xref_object(xref)) #string
#     print('\n')
import fitz

# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document('..\\..\\..\\pdf\\fit\\24420.pdf')
# -------------------------------------------------------------------------------------------

page = doc[20]

#imageBlock_dict: dict_keys(['number', 'type', 'bbox', 'width', 'height', 'ext', 'colorspace', 'xres', 'yres', 'bpc', 'transform', 'size', 'image'])
#   |-> Key "type": 1 = image (int)
#   |-> Possible values of the “ext” key are “bmp”, “gif”, “jpeg”, “jpx” (JPEG 2000), “jxr” (JPEG XR), “png”, “pnm”, and “tiff”.
#textBlock_dict: dict_keys(['number', 'type', 'bbox', 'lines'])
#   |-> Key "type": 0 = text (int)

# if origin y is the same => one line

# font flags: 0bBMSIX -> B - bold; M - monospaced; S - serifed; I - italic; X - superscripted – not a font property, detected by MuPDF code.


WIDTH = 150

dictionary = page.get_text("dict")
#print(dictionary)
blocks = dictionary['blocks']
#print(blocks[10]['ext'])
print(" " + WIDTH*"-")
for block in blocks:
    print("|" + WIDTH*" " + "|")
    #print(block)
    #input()
    if block['type'] == 0:
        lines = block['lines']
        for line in lines:
            #print(line)
            for span in line['spans']:
                print("| " + span['text'] + (WIDTH-1-len(span['text']))*" " + "|")
                print("| " + str(line['bbox']) + "    font: " + span['font'] + "    size: "  + str(span['size']) + "   flags: " + str(bin(span['flags'])) + (WIDTH-1-len(str(line['bbox']))-10-len(span['font'])-10-len(str(span['size']))-10-len(str(bin(span['flags']))))*" " + "|")
    else: #type = 1
        print(block['ext'])
        print(block['size'])
        print(block['transform'])
    print("|" + WIDTH*" " + "|")
    print(" " + WIDTH*"-")

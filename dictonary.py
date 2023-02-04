import fitz

# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("projekt.pdf")
# -------------------------------------------------------------------------------------------

page = doc[3]

#imageBlock_dict: dict_keys(['number', 'type', 'bbox', 'width', 'height', 'ext', 'colorspace', 'xres', 'yres', 'bpc', 'transform', 'size', 'image'])
#   |-> Key "type": 1 = image (int)
#   |-> Possible values of the “ext” key are “bmp”, “gif”, “jpeg”, “jpx” (JPEG 2000), “jxr” (JPEG XR), “png”, “pnm”, and “tiff”.
#textBlock_dict: dict_keys(['number', 'type', 'bbox', 'lines'])
#   |-> Key "type": 0 = text (int)

# if origin y is the same => one line

dictionary = page.get_text("dict")
#print(dictionary)
blocks = dictionary['blocks']
#print(blocks[10]['ext'])
print(" ------------------------------------------------------------------------------------------")
for block in blocks:
    print("|                                                                                          |")
    #print(block)
    #input()
    if block['type'] == 0:
        lines = block['lines']
        for line in lines:
            #print(line)
            for span in line['spans']:
                print("| " + span['text'] + (89-len(span['text']))*" " + "|")
            print("| " + str(line['bbox']) + (89-len(str(line['bbox'])))*" " + "|")
    else: #type = 1
        print(block['ext'])
        print(block['size'])
    print("|                                                                                          |")
    print(" ------------------------------------------------------------------------------------------")

import fitz

# ------------------------------------ DOPLNIT ----------------------------------------------
doc = fitz.Document("C:\\Users\\micha\\Desktop\\Michaela\\Skola\\VS\\bakalarka\\pdf\\overflow.pdf")
# -------------------------------------------------------------------------------------------

for page in doc:
    potential_x2 = []
    
    dictionary = page.get_text("dict")
    blocks = dictionary['blocks']
    for block in blocks:
        print("")
        print("====== NEW BLOCK ======")
        print()
        if block['type'] == 0:
            lines = block['lines']
            if len(lines) > 1:
                origin_y = -1.0
                origin_x = -1.0
                for line in lines:
                    print("== new line ==")
                    print()
                    line_origin = line['spans'][0]['origin']
                    if line_origin[1] == origin_y:
                        # not a new line, just tab -> pop previous
                        print("--- popping previous")
                        potential_x2.pop()
                    else:
                        if line_origin[0] > origin_x and origin_x != -1.0:
                            # new paragraph
                            potential_x2.pop() #pop the last line in previous paragraph
                            print("--- popping last line in previous par")
                        origin_x = line_origin[0]
                    origin_y = line_origin[1]
                    potential_x2.append(line['bbox'][2])
                    print("--- appending:")
                    print(line['spans'][0]['text'])
                    print()
                potential_x2.pop() #pop the last line in paragraph
                print("--- popping last line")
                print(potential_x2)
        else: #type = 1
            potential_x2.append(block['bbox'][2])
            print("--- appending image")

    print(potential_x2)
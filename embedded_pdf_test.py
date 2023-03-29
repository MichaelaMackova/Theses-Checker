import sys
import random
import numpy
import fitz

# ---------------------------------------------- MAIN --------------------------------------------------------

if len(sys.argv) != 2 or sys.argv[1] == "-h":
    print("Description:")
    print("\tMakes a new pdf file called 'annotated.pdf' in the folder, where this program is saved.")
    print()
    print("Usage:\t\tpython .\\small_image_test.py <PDFfilePath>")
    print("For example:\tpython .\\small_image_test.py .\\pdf\\check.pdf")
    print()
    exit()


doc = fitz.Document(sys.argv[1])

for page in doc:

    tmp_xobjects = page.get_xobjects()
    xobjects = []
    for xobject in tmp_xobjects:
        # xobject = (xref, name, invoker, bbox)
        if xobject[2] == 0:
            # page directly invokes this xobject
            xobjects.append(xobject)


    pageContent = str(page.read_contents(),'utf-8')
    cmds = pageContent.splitlines()

    embeddedPdfBlocks = []
    CTMStack = []

    CTM = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]

    for cmd in cmds:

        if cmd == 'q':
            CTMStack.append(CTM)
        elif cmd == 'Q':
            CTM = CTMStack.pop()
        elif cmd[-2:] == 'cm':
            matrix = cmd.split(' ')
            cm = [
                [float(matrix[0]), float(matrix[1]), 0.0],
                [float(matrix[2]), float(matrix[3]), 0.0],
                [float(matrix[4]), float(matrix[5]), 1.0]
            ]
            CTM = numpy.matmul(cm,CTM)
        elif cmd[-2:] == 'Do':
            for xobject in xobjects:
                # xobject = (xref, name, invoker, bbox)
                if cmd == "/" + xobject[1] + " Do":
                    pageTransMatrix = [
                        [page.transformation_matrix.a, page.transformation_matrix.b, 0.0],
                        [page.transformation_matrix.c, page.transformation_matrix.d, 0.0],
                        [page.transformation_matrix.e, page.transformation_matrix.f, 1.0]
                    ] # flips upside down - (0,0) in view is top-left, but in internal pdf is bottom-left
                    viewMatrix = numpy.matmul(CTM,pageTransMatrix)
                    # [ x' y' 1 ] = [ x  y  1 ] * viewMatrix
                    blMatrix = numpy.matmul([xobject[3][0], xobject[3][1], 1.0],viewMatrix)
                    trMatrix = numpy.matmul([xobject[3][2], xobject[3][3], 1.0],viewMatrix)
                    embeddedPdfBlocks.append(
                        {
                            'type'          : 1,
                            'bbox'          : fitz.Rect(blMatrix[0], trMatrix[1], trMatrix[0], blMatrix[1]),
                            'ext'           : 'pdf',
                            'width'         : xobject[3].width,
                            'height'        : xobject[3].height,
                            'colorspace'    : None,
                            'xres'          : None,
                            'yres'          : None,
                            'bpc'           : None,
                            'transform'     : fitz.Matrix(CTM[0][0], CTM[0][1], CTM[1][0], CTM[1][1], CTM[2][0], CTM[2][1]),
                            'size'          : int(doc.xref_get_key(xobject[0],'Length')[1]),
                            'image'         : doc.xref_stream_raw(xobject[0])
                        }
                    )
                    break




    for pdfImage in embeddedPdfBlocks:
        page.add_highlight_annot(pdfImage['bbox'])

doc.save("annotated.pdf")
#----------------------------------------------------------------------------
# File          : theses_checker.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 14.1.2023
# Last Updated  : 19.10.2024
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

import string
import random
from statistics import median
import fitz
import re
from enum import Enum
import numpy



# NOT USED
class Language(Enum):
    CZECH = 0
    SLOVAK = 1
    ENGLISH = 2
    


class Checker:
    ## Maximum count of pages scanned to find general information of the document
    RND_PAGE_CNT = 10
    ## Red color for highlighting. RGB format.  
    HIGH_RED = (255, 128, 128)
    ## Orange color for highlighting. RGB format.  
    HIGH_ORANGE = (253, 182, 116)
    ## Padding for highlight used in overflow check.
    HIGHLIGHT_PADDING = 1.5
    ## Red color in RGB format.  
    RED = (204, 0, 0)
    ## White color in RGB format.  
    WHITE = (255, 255, 255)

    def __init__(self, pdfPath : string, pdfLang : Language = None):
        """
        Constructor. Creates a document that can be checked for mistakes.

        Args:
            pdfPath (string): Path to the PDF, that will be checked.
            pdfLang (Language, optional): Language of PDF content. Defaults to None. (Not used)
        """
        ## Boolean indicating whether during check, anything was marked as mistake
        self.mistakes_found = False
        ## Boolean indicating whether during finding page border was successful 
        self.borderNotFound = False
        ## Scanned PDF Document
        self.__document = fitz.Document(pdfPath)
        ## Currently scanned page
        self.__currPage = fitz.Page
        ## TextPage of current page
        self.__currTextPage = fitz.TextPage
        ## Pixmap of current page
        self.__currPixmap = fitz.Pixmap
        ## Dictionary of current page
        self.__currDict = None
        ## List of embedded PDFs invoked by current page as dictionary image blocks 
        self.__currPageEmbeddedPdfs = None
        ## All text from current page in one continuous string (warning: included text from embedded PDFs)
        self.__currPageTextContent = None
        ## Tuple containing x0 and x1 coordinates of page border
        self.__border = (-1.0, -1.0)
        ## Boolean indicating whether current page contains table of content (TOC)
        self.__isContentPage = False
        ## Language of document (Not used)
        self.__language = pdfLang
        ## Default font used in document
        self.__regularFont = None
        ## Boolean indicating whether previous block contains a heading
        self.__isPreviousTitle = False
        ## Boolean indicating whether embedded PDFs inside document will be taken as images
        self.__embeddedPdfAsImage = True
        


    def __rgbToPdf(self, color:tuple):
        """
        Converts color from RGB format to PDF format.

        Args:
            color (tuple): Color in RGB format, for example (255, 128, 128).

        Returns:
            tuple: Color in format to use in PDF.
        """
        return (color[0]/255.0, color[1]/255.0, color[2]/255.0)



    def __randomPagesIndex(self):
        """
        Returns maximum of RND_PAGE_CNT count of indexes of random pages.

        Returns:
            list: Indexes of random pages.
        """
        docLen = len(self.__document)
        if docLen <= 5:
            return range(0, docLen)
        maxListLen = min(self.RND_PAGE_CNT, docLen-4)
        return random.sample(range(2, docLen-2), maxListLen)



    def __highlight(self, rects:list, color:tuple, text:string = None, title:string = None):
        """
        Adds highlight annotation. If text is specified adds a pop-up window.

        Args:
            rects (list): List of rectangles to be highlighted.
            color (tuple): RGB representation of highlight color.
            text (string, optional): Text that will be shown in the pop-up annotation. Defaults to None.
            title (string, optional): Title of the pop-up annotation. Defaults to None.
        """
        if len(rects) > 0:
            
            annot = self.__currPage.add_highlight_annot(rects)
            annot.set_colors(stroke=self.__rgbToPdf(color))

            if text != None:
                info = annot.info
                if title != None:
                    info["title"] = title
                info["content"] = text
                annot.set_info(info)

            annot.update()



    def __overflowLine(self, x:float, overflow_rects:list):
        """
        Draws a vertical line(s) at x. Start and end y is specified by overflow_rect's y0 and y1.
        Line will be longer by 20 on each side.

        Args:
            x (float): X coordinate, where line is located.
            overflow_rects (list): List of rectangles, that specify y coordinates of line(s).
        """
        for rect in overflow_rects:
            annot = self.__currPage.add_line_annot(fitz.Point(x,rect[1]-20), fitz.Point(x,rect[3]+20))
            annot.set_border(width=1)
            annot.set_colors(stroke=self.__rgbToPdf(self.RED))
            annot.update()



    def __getPageXobjects(self):
        """
        Gets non-image XObjects invoked by current page.

        Returns:
            list: XObjects invoked by current page. Every XObject is a tuple (xref, name, invoker, bbox).
        """
        tmp_xobjects = self.__currPage.get_xobjects()
        xobjects = []
        for xobject in tmp_xobjects:
            # xobject = (xref, name, invoker, bbox)
            if xobject[2] == 0:
                # page directly invokes this xobject
                xobjects.append(xobject)

        return xobjects



    def __getPageEmbeddedPdfs(self):
        """
        Updates class variable currPageEmbeddedPdfs.
        """
        if self.__currPageEmbeddedPdfs != None:
            # instance already exists
            return
        
        self.__currPageEmbeddedPdfs = []
        xobjects = self.__getPageXobjects()
        embeddedPdfBlocks = []
        if xobjects:
            try:
                pageContent = str(self.__currPage.read_contents(),'utf-8')
            except:
                return
            cmds = pageContent.splitlines()

            CTMStack = []
            CTM = [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]
            ]

            for cmd in cmds:
                if cmd[-1:] == 'q':
                    CTMStack.append(CTM)
                elif cmd[-1:] == 'Q':
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
                            CTMStack.append(CTM)

                            Matrix = self.__document.xref_get_key(xobject[0], "Matrix")[1]
                            if Matrix != 'null':
                                #Matrix = '[a b c d e f]'
                                Matrix = Matrix[1:-1]
                                Matrix = Matrix.split(" ")
                                Matrix = [
                                    [float(Matrix[0]), float(Matrix[1]), 0.0],
                                    [float(Matrix[2]), float(Matrix[3]), 0.0],
                                    [float(Matrix[4]), float(Matrix[5]), 1.0]
                                ]
                                CTM = numpy.matmul(Matrix,CTM)

                            pageTransMatrix = [
                                [self.__currPage.transformation_matrix.a, self.__currPage.transformation_matrix.b, 0.0],
                                [self.__currPage.transformation_matrix.c, self.__currPage.transformation_matrix.d, 0.0],
                                [self.__currPage.transformation_matrix.e, self.__currPage.transformation_matrix.f, 1.0]
                            ] # flips upside down - (0,0) in view is top-left, but in internal pdf is bottom-left
                            viewMatrix = numpy.matmul(CTM,pageTransMatrix)
                            # [ x' y' 1 ] = [ x  y  1 ] * viewMatrix
                            blMatrix = numpy.matmul([xobject[3][0], xobject[3][1], 1.0],viewMatrix)
                            trMatrix = numpy.matmul([xobject[3][2], xobject[3][3], 1.0],viewMatrix)

                            length = self.__document.xref_get_key(xobject[0],'Length')
                            if length[0] == 'xref':
                                length_xref = length[1][:-4] # always ends with ' 0 R'
                                size = self.__document.xref_object(int(length_xref))
                                size = int(size)
                            elif length[0] == 'int':
                                size = int(length[1])
                            elif length[0] == 'string':
                                try:
                                    size = int(length[1])
                                except:
                                    size = None
                            else:
                                size = None
                                
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
                                    'size'          : size,
                                    'image'         : self.__document.xref_stream_raw(xobject[0])
                                }
                            )

                            CTM = CTMStack.pop()
                            break
        self.__currPageEmbeddedPdfs = sorted(embeddedPdfBlocks, key=lambda x: (x['bbox'][1], x['bbox'][0]))



    def __getTextPage(self):
        """
        Gets current TextPage from current page.
        """
        if self.__currTextPage == None:
            self.__currTextPage = self.__currPage.get_textpage()



    def __rectRelativePosition(self, rectA, rectB):
        """
        Determines relative position of two rectangles, top-to-bottom (biggest priority) then left-to-right.

        Args:
            rectA: One of two rectangles, which position is determined.
            rectB: One of two rectangles, which position is determined.

        Returns:
            int: Relative position of two rectangles.
                -1 -> rectA before rectB,
                0 -> rectA inside rectB,
                1 -> rectA after rectB
        """
        if rectA[0]>=rectB[0] and rectA[1]>=rectB[1] and rectA[2]<=rectB[2] and rectA[3]<=rectB[3]:
            return 0
        elif rectA[1]<rectB[1]:
            return -1
        elif rectA[1]==rectB[1] and rectA[0]<rectB[0]:
            return -1
        else:
            return 1



    def __isInsideEmbeddedPdf(self, rect):
        """
        Determines if specified rectangle is inside any of embedded PDFs on current page.

        Args:
            rect: Rectangle which position is determined.

        Returns:
            bool: Position of specified rectangle.
        """
        self.__getPageEmbeddedPdfs()
        for embeddedPdfBlock in self.__currPageEmbeddedPdfs:
            if self.__rectRelativePosition(rect, embeddedPdfBlock['bbox']) == 0:
                return True
        return False



    def __replaceBlocksByEmbeddedPdfs(self):
        """
        Replaces current dictionary blocks, that belong to embedded PDFs, with image blocks.
        """
        self.__getPageEmbeddedPdfs()
        embeddedPdfBlocks = self.__currPageEmbeddedPdfs.copy()
        if embeddedPdfBlocks:
            blocks = self.__currDict['blocks']
            idx = 0
            while idx < len(blocks) and embeddedPdfBlocks:
                position = self.__rectRelativePosition(blocks[idx]['bbox'], embeddedPdfBlocks[0]['bbox'])
                if position == 0:
                        blocks.pop(idx)
                        idx = idx - 1
                elif position == 1:
                    blocks.insert(idx,embeddedPdfBlocks.pop(0))
                idx = idx + 1

            for pdfBlock in embeddedPdfBlocks:
                blocks.append(pdfBlock)
            self.__currDict['blocks'] = blocks



    def __getPageDictionary(self):
        """
        Gets current dictionary of current page.
        """
        if self.__currDict == None:
            self.__getTextPage()
            self.__currDict = self.__currPage.get_text("dict", textpage=self.__currTextPage, sort=True)
            if self.__embeddedPdfAsImage:
                self.__replaceBlocksByEmbeddedPdfs()



    def __getPageBorder(self):
        """
        Examines current page and determines its left and right border.

        Returns:
            tuple: Left and right border of examined page in the form of tuple containing two float numbers: (xLeft, xRight).
        """
        potentialLeft = []
        potentialRight = []
        
        self.__getPageDictionary()
        blocks = self.__currDict['blocks']

        for block in blocks:

            if block['type'] == 0: 
                # --- text ---
                lines = block['lines']

                if len(lines) > 1:  # multiline text
                    origin_y = -1.0
                    origin_x = -1.0

                    for line in lines:
                        if line['spans']:
                            line_origin = line['spans'][0]['origin']

                            if line_origin[1] == origin_y:
                                # not a new line, just tab -> pop previous right border
                                potentialRight.pop()
                            else:
                                potentialLeft.append(line['bbox'][0])

                                if line_origin[0] > origin_x and origin_x != -1.0:
                                    # new paragraph
                                    potentialRight.pop() #pop the last line in previous paragraph
                                    potentialLeft.pop() #pop this line -> indent

                                origin_x = line_origin[0]

                            origin_y = line_origin[1]
                            potentialRight.append(line['bbox'][2])

                    potentialRight.pop() #pop the last line in paragraph

            else: #type = 1
                # --- image ---
                potentialLeft.append(block['bbox'][0])
                potentialRight.append(block['bbox'][2])

        xLeft = -1.0
        if potentialLeft:
            xLeft = median(potentialLeft)

        xRight = -1.0
        if potentialRight:
            xRight = median(potentialRight)
        
        return (xLeft, xRight)

    

    def __getFontIndex(self, fonts : list, font : dict):
        """
        Finds index of specified font inside a list of fonts.

        Args:
            fonts (list): List of fonts where search occurs.
            font (dict): Searched font.

        Returns:
            int|None: Index of specified font. If not found returns None.
        """
        for i in range(len(fonts)):
            currFont = fonts[i]
            if not isinstance(currFont,dict):
                currFont = fonts[i][0]
            if ((currFont['name'] == font['name']) and (currFont['size'] == font['size']) and (currFont['flags'] == font['flags'])):
                return i
        return None

    

    def __getPageUsedFonts(self):
        """
        Returns a list of all fonts used on current page.

        Returns:
            list: List of all used font. One element = ({'name', 'size', 'flags'}, total_character_count).
        """
        fonts = []

        self.__getPageDictionary()
        blocks = self.__currDict['blocks']

        for block in blocks:
            if block['type'] == 0: 
                # --- text ---
                lines = block['lines']
                for line in lines:
                    spans = line['spans']
                    for span in spans:
                        font = dict(name=span['font'], size=round(span['size'],5), flags=span['flags'])
                        index = self.__getFontIndex(fonts,font)
                        if index != None:
                            fonts[index] = (font, fonts[index][1] + len(span['text']))
                        else:
                            fonts.append((font,len(span['text'])))
        return fonts

    

    def __getMostUsedFontIndex(self, fonts : list):
        """
        Finds index of the most used font in list of fonts.

        Args:
            fonts (list): List of fonts. One element should be (font, total_character_count).

        Returns:
            int: Index of most used font.
        """
        index_mostUsedFont = 0
        for index in range(1,len(fonts)):
            if fonts[index][1] > fonts[index_mostUsedFont][1]:
                index_mostUsedFont = index
        return index_mostUsedFont

    

    def __getPageRegularFont(self):
        """
        Gets general font used on current page.

        Returns:
            tuple: Regular font of current page with the layout: ({'name', 'size', 'flags'}, total_character_count)
        """
        fonts = self.__getPageUsedFonts() 
        if not fonts:
            return None
        return fonts[self.__getMostUsedFontIndex(fonts)]

    

    def __getDocInfo(self, findBorder : bool, findRegularFont : bool):
        """
        Scans random pages of document and determines general information of the document needed for some checks.

        Args:
            findBorder (bool): Determines if border of page will be searched for.
            findRegularFont (bool): Determines if regular font of document will be searched for.
        """
        right_borders = []
        left_borders = []
        regularFonts = []
        rnd_page_i = self.__randomPagesIndex()

        self.__resetCurrVars()

        for i in rnd_page_i:
            self.__currPage = self.__document[i]

            if findBorder:
                leftX, rightX = self.__getPageBorder()
                right_borders.append(rightX)
                left_borders.append(leftX)

            if findRegularFont:
                font = self.__getPageRegularFont()
                if font:
                    index = self.__getFontIndex(regularFonts, font[0])
                    if index != None:
                        regularFonts[index] = (font[0], regularFonts[index][1] + font[1])
                    else:
                        regularFonts.append(font)

            self.__resetCurrVars()

        if findBorder:
            borderLeft = median(left_borders)
            borderRight = median(right_borders)
            if (borderLeft < borderRight) and (borderLeft != -1.0) and (borderRight != -1.0):
                self.__border = (borderLeft, borderRight)
            else:
                # bad border found
                self.borderNotFound = True
                pageBound = self.__document[0].rect
                if (borderLeft != -1.0) and (borderRight == -1.0):
                    self.__border = (borderLeft, pageBound[2])
                elif (borderLeft == -1.0) and (borderRight != -1.0):
                    self.__border = (pageBound[0], borderRight)
                else:
                    self.__border = (pageBound[0], pageBound[2])

        if findRegularFont:
            self.__regularFont = regularFonts[self.__getMostUsedFontIndex(regularFonts)][0] if regularFonts else None



    def __getPixmap(self):
        """
        Gets current Pixmap from current page.
        """
        if self.__currPixmap == None:
            self.__currPixmap = self.__currPage.get_pixmap()



    def __getPageRightOverflow(self):
        """
        Scans a page and returns where overflow happened on the right side of current page.

        Returns:
            list: List of rectangles where overflow was detected.
        """
        self.__getPixmap()
        overflow_rects = [None]
        r_border = round(self.__border[1])
        y = 0
        while y < self.__currPixmap.height:
            x = self.__currPixmap.width - 1
            while x > r_border:
                if self.__currPixmap.pixel(x,y) != self.WHITE:

                    if overflow_rects[-1] == None:
                        # previous line was only WHITE
                        overflow_rects.pop()
                        overflow_rects.append([r_border+1,y-self.HIGHLIGHT_PADDING,x+self.HIGHLIGHT_PADDING,y+self.HIGHLIGHT_PADDING])
                    else: 
                        # previous line had overflow -> merge rectanles
                        overflow_rects[-1][2] = max(overflow_rects[-1][2],x+self.HIGHLIGHT_PADDING)
                        overflow_rects[-1][3] = y+self.HIGHLIGHT_PADDING
                    break
                x = x - 1
            
            if x == r_border and overflow_rects[-1] != None:
                # if whole line was WHITE and previous line wasn't
                overflow_rects.append(None)
            y = y + 1

        if overflow_rects[-1] == None:
            overflow_rects.pop()
        
        return overflow_rects



    def __getPageLeftOverflow(self):
        """
        Scans a page and returns where overflow happened on the left side of current page.

        Returns:
            list: List of rectangles where overflow was detected.
        """
        self.__getPixmap()
        overflow_rects = [None]
        l_border = round(self.__border[0]) - 1
        y = 0
        while y < self.__currPixmap.height:
            x = 0
            while x < l_border:
                if self.__currPixmap.pixel(x,y) != self.WHITE:

                    if overflow_rects[-1] == None:
                        # previous line was only WHITE
                        overflow_rects.pop()
                        overflow_rects.append([x-self.HIGHLIGHT_PADDING,y-self.HIGHLIGHT_PADDING,l_border,y+self.HIGHLIGHT_PADDING])
                    else: 
                        # previous line had overflow -> merge rectanles
                        overflow_rects[-1][0] = min(overflow_rects[-1][0],x-self.HIGHLIGHT_PADDING)
                        overflow_rects[-1][3] = y+self.HIGHLIGHT_PADDING
                    break
                x = x + 1
            
            if x == l_border and overflow_rects[-1] != None:
                # if whole line was WHITE and previous line wasn't
                overflow_rects.append(None)
            y = y + 1

        if overflow_rects[-1] == None:
            overflow_rects.pop()
        
        return overflow_rects



    def __overflowPageCheck(self):
        """
        Check for overflow on left and right side of current page. Highlights all spaces where overflow occurred.
        """
        overflow_rects = self.__getPageRightOverflow()
        self.__highlight(overflow_rects,self.HIGH_RED)
        self.__overflowLine(self.__border[1], overflow_rects)
        if(overflow_rects):
            self.mistakes_found = True
        overflow_rects = self.__getPageLeftOverflow()
        self.__highlight(overflow_rects,self.HIGH_RED)
        self.__overflowLine(self.__border[0], overflow_rects)
        if(overflow_rects):
            self.mistakes_found = True



    def __searchForAndHighlight(self, searchFor : string, popupText : string, popupTitle:string = "Chyba / Error", highlightColor:tuple = HIGH_RED):
        """
        Searches for searchFor expression on current page and highlights all occurrences.

        Args:
            searchFor (string): Expression that will be searched for.
            popupText (string): Text that will be shown in the pop-up annotation attached to highlight annotation.
            popupTitle (string, optional): Title of the pop-up annotation attached to highlight annotation. Defaults to "Chyba / Error".
            highlightColor (tuple, optional): RGB representation of highlight color. Defaults to HIGH_RED.
        """
        self.__getTextPage()
        rects = self.__currPage.search_for(searchFor, textpage=self.__currTextPage)
        for rect in rects:
            if rect.is_valid and rect[0] < rect[2] and rect[1] < rect[3]:
                if self.__embeddedPdfAsImage:
                    if self.__isInsideEmbeddedPdf(rect):
                        continue
                self.mistakes_found = True
                self.__highlight(rect, highlightColor, popupText, popupTitle)



    def __hyphenPageCheck(self):
        """
        Check for wrong usage of hyphen on current page. Highlights all bad usages.
        """
        self.__searchForAndHighlight(" - ", "Pouzijte pomlcku namisto spojovniku. / Use dash instead of hyphen.", "Chyba / Error", self.HIGH_RED)



    def __doubleQuestionMarkPageCheck(self):
        """
        Check for missing references on current page, which are indicated by '??'. Highlights all missing references.
        """
        self.__searchForAndHighlight("??", "Spatne uvedena reference. / Missing reference.", "Chyba / Error", self.HIGH_RED)



    def __drawArrow(self,x_pointing:float,x:float,y:float):
        """
        Draws horizontal arrow annotation.

        Args:
            x_pointing (float): Start coordinate of arrow. Point of the arrow will be at this coordinate.
            x (float): End coordinate of arrow.
            y (float): Vertical position of arrow.
        """
        S = 2
        annot = self.__currPage.add_line_annot(fitz.Point(x_pointing,y), fitz.Point(x,y))
        annot.set_border(width=1)
        annot.set_colors(stroke=self.__rgbToPdf(self.RED))
        annot.update()

        if (x_pointing > x ):
            S *= -1
        annot = self.__currPage.add_line_annot(fitz.Point(x_pointing,y), fitz.Point(x_pointing+S*2.5,y-S))
        annot.set_border(width=1)
        annot.set_colors(stroke=self.__rgbToPdf(self.RED))
        annot.update()

        annot = self.__currPage.add_line_annot(fitz.Point(x_pointing,y), fitz.Point(x_pointing+S*2.5,y+S))
        annot.set_border(width=1)
        annot.set_colors(stroke=self.__rgbToPdf(self.RED))
        annot.update()



    def __imageWidthPageCheck(self):
        """
        Check width of all images on current page. Marks all images with width 85% to 99% of line width.
        """
        lineWidth = self.__border[1] - self.__border[0]
        rects = []
        self.__getPageDictionary()
        blocks = self.__currDict['blocks']

        for block in blocks:
            if block['type'] == 1:
                imageBox = block['bbox']

                imageWidth = imageBox[2] - imageBox[0]
                percentage = (imageWidth * 100.0)/lineWidth
                

                if percentage > 85.0 and percentage < 99.0:
                    rects.append(imageBox)
                    y = (imageBox[3]-imageBox[1])/2.0 + imageBox[1]
                    self.__drawArrow(self.__border[0],imageBox[0],y)
                    self.__drawArrow(self.__border[1],imageBox[2],y)
        
        if rects:
            self.mistakes_found = True
        self.__overflowLine(self.__border[0],rects)
        self.__overflowLine(self.__border[1],rects)



    def __getIsContentPage(self, pageFirstBlock : dict):
        """
        Updates isContentPage class variable.

        Args:
            pageFirstBlock (dict): First block from dictionary of current page.
        """
        if (pageFirstBlock['type'] == 0): 
            # --- text ---
            lines = pageFirstBlock['lines']
            if (len(lines) == 1):
                #contentText = "Obsah" if (self.__language == Language.CZECH or self.__language == Language.SLOVAK) else "Contents"
                line_spans = lines[0]['spans']
                if line_spans:
                    text = line_spans[0]['text'].lower().strip()
                    if ( text == "obsah" or text == "contents"):
                        self.__isContentPage = True
                    else:
                        self.__isContentPage = False



    def __TOCSectionsCheck(self):
        """
        Checks if current page contains table of content (TOC). Check for headings of level 3 or higher in TOC.
        Highlights all headings of level 3 or higher in TOC.
        """
        self.__getPageDictionary()
        blocks = self.__currDict['blocks']
        if blocks:
            self.__getIsContentPage(blocks[0])
            if (self.__isContentPage):
                for block in blocks:
                    if block['type'] == 0: 
                        # --- text ---
                        lines = block['lines']
                        origin_y = -1.0
                        for line in lines:
                            if not line['spans']:
                                continue
                            
                            line_origin = line['spans'][0]['origin']
                            if line_origin[1] != origin_y:
                                # new line, not tab -> section number
                                x = re.search("^(?:\d+|[A-Z])\.(?:\d+\.)+\d+", line['spans'][0]['text']) # example: 3.12.5; C.2.3
                                if x:
                                    self.mistakes_found = True
                                    self.__highlight([line['bbox']],self.HIGH_RED,"Nadpisy 3 a vetsi urovne nezobrazovat v obsahu. / Do not show headings level 3 or more in table of content", "Chyba / Error")
                            origin_y = line_origin[1]



    def __deleteDuplicate(self, array : list):
        """
        Deletes all duplicates inside an array.

        Args:
            array (list): List where duplicates are deleted.

        Returns:
            list: List with only unique instances.
        """
        return list(dict.fromkeys(array))



    def __getPageTextContent(self):
        """
        Scans current page for all text and saves its dehyphenated form in class variable currPageTextContent (warning: text from embedded PDFs included)
        """
        if self.__currPageTextContent == None:
            self.__currPageTextContent = ""
            textBlocks = self.__currPage.get_text("blocks", flags=fitz.TEXT_PRESERVE_LIGATURES|fitz.TEXT_DEHYPHENATE|fitz.TEXT_MEDIABOX_CLIP)
            for block in textBlocks:
                text = ""
                # block = (x0, y0, x1, y1, "lines in the block", block_no, block_type)
                if block[6] == 0:   # contains text
                    text = block[4]
                    if text[-1] == "\n":
                        text = text[:-1]
                    
                    self.__currPageTextContent += text.replace("\n"," ") + "\n\n"




    def __regexSearchAndHighlight(self, regexSearch : string, popupText:string, popupTitle:string = "Chyba / Error", highlightColor:tuple = HIGH_RED):
        """
        Searches for regexSearch as a regular expression on current page and highlights all occurrences.

        Args:
            regexSearch (string): Regular expression that will be searched for.
            popupText (string): Text that will be shown in the pop-up annotation attached to highlight annotation.
            popupTitle (string, optional): Title of the pop-up annotation attached to highlight annotation. Defaults to "Chyba / Error".
            highlightColor (tuple, optional): RGB representation of highlight color. Defaults to HIGH_RED.
        """
        self.__getPageTextContent()
        matchList = re.findall(regexSearch, self.__currPageTextContent)

        if matchList:
            matchList = self.__deleteDuplicate(matchList)
            for match in matchList:
                self.__searchForAndHighlight(match, popupText, popupTitle, highlightColor)



    def __spaceBracketCheck(self):
        """
        Check for missing space before any left bracket on current page. Highlights all missing spaces.
        """
        # "\S(?:\(|\[|{)" -> for example: "l(", ".[", "5{"
        self.__regexSearchAndHighlight("\S(?:\(|\[|{)", "Chybi mezera pred levou zavorkou. / Missing space in between.", "Varovani / Warning", self.HIGH_ORANGE)
        


    def __isTitleBlock(self, blockNumber : int):
        """
        Examines if a block from current dictionary contains a title of (sub)section.

        Args:
            blockNumber (int): Index of current dictionary block which is examined.

        Returns:
            bool: Whether the examined block contains a title of (sub)section.
        """
        block = self.__currDict['blocks'][blockNumber]
        block_info = dict(linesCount=0, fonts=[])
        if block['type'] == 0:
            # --- text ---
            lines = block['lines']
            block_info['linesCount'] = len(lines)
            origin_y = -1.0
            for line in lines:
                spans = line['spans']
                if spans:
                    line_origin = spans[0]['origin']
                    if line_origin[1] == origin_y:
                        # not a new line
                        block_info['linesCount'] -= 1
                    origin_y = line_origin[1]
                    
                    for span in spans:
                        font = dict(name=span['font'], size=round(span['size'],5), flags=span['flags'])
                        index = self.__getFontIndex(block_info['fonts'],font)
                        if index == None:
                            block_info['fonts'].append(font)
            
            if self.__getFontIndex(block_info['fonts'],self.__regularFont) == None:
                if len(block_info['fonts']) > 2:
                    return False
                for font in block_info['fonts']:
                    if font['size'] < self.__regularFont['size']:
                        return False
                return True
        return False



    def __getBlockText(self, blockNumber : int):
        """
        Extracts all text from one block in current dictionary.

        Args:
            blockNumber (int): Index of block where text will be extracted.

        Returns:
            str: Text from the block of current dictionary.
        """
        self.__getPageDictionary()
        block = self.__currDict['blocks'][blockNumber]
        text = ""
        if block['type'] == 0:
            origin_y = -1.0
            origin_x = -1.0
            lines = block['lines']
            for line in lines:
                spans = line['spans']
                if spans:
                    line_origin = spans[0]['origin']
                    if line_origin[1] == origin_y:
                        # not a new line
                        text = text[:-1] + "\t"
                    else:
                        if line_origin[0] > origin_x and origin_x != -1.0:
                            # new paragraph
                            text = text[:-1] + "\n"
                    origin_y = line_origin[1]
                    origin_x = line_origin[0]
                    
                    for span in spans:
                        text += span['text']
                    if text[-1] == "-":
                        text = text[:-1]
                    else:
                        text+=" "
            text=text[:-1]
        return text



    def __emptySectionCheck(self):
        """
        Check for absence of text between (sub)section titles on current page. Highlights all empty (sub)sections.
        """
        isPreviousNewChapterTitle=False
        self.__getPageDictionary()
        blocks = self.__currDict['blocks']
        for blockNumber in range(len(blocks)):
            if self.__isTitleBlock(blockNumber):
                blockText = self.__getBlockText(blockNumber)
                x = re.search("\t\d+$", blockText) # example: Úvod   2
                if self.__isPreviousTitle and not isPreviousNewChapterTitle and not x:
                    y1=blocks[blockNumber-1]['bbox'][3]
                    y2=blocks[blockNumber]['bbox'][1]
                    if y1 < y2:
                        rect = fitz.Rect(self.__border[0],y1,self.__border[1],y2)
                        if rect.is_valid and rect[0] < rect[2] and rect[1] < rect[3]:
                            self.mistakes_found = True
                            self.__highlight([rect],self.HIGH_RED,"Chybi text mezi nadpisy. / Missing text between sections.","Chyba / Error")

                x = re.search("^(?:(?:Kapitola|Chapter) \d+|(?:Příloha|Appendix|Príloha) [A-Z])$", blockText) # example: Kapitola 4; Chapter 4; Appendix D; Príloha D; Příloha D
                if  x:
                    isPreviousNewChapterTitle = True
                else:
                    isPreviousNewChapterTitle = False
                self.__isPreviousTitle = True
            else:
                isPreviousNewChapterTitle = False
                self.__isPreviousTitle = False



    def __resetCurrVars(self):
        """
        Resets all class variables starting with "curr".
        """
        self.__currPage = None
        self.__currDict = None
        self.__currPixmap = None
        self.__currTextPage = None
        self.__currPageEmbeddedPdfs = None
        self.__currPageTextContent = None


    
    def __resetCheckerVars(self):
        """
        Resets all class variables for new annotating.
        """
        self.__resetCurrVars()
        self.mistakes_found = False
        self.borderNotFound = False
        self.__border = (-1.0, -1.0)
        self.__isContentPage = False
        self.__regularFont = None
        self.__isPreviousTitle = False



    def isFileEmpty(self):
        """
        Checks if file has any pages -> if file can be parsed.

        Returns:
            bool: True -> file cannot be parsed; False -> file can be parsed
        """
        return not self.__document



    def annotate(self ,annotatedPath : string, embeddedPdfAsImage : bool = True, borderCheck : bool = True, hyphenCheck : bool = True, imageWidthCheck : bool = True,
                 TOCCheck : bool = True, spaceBracketCheck : bool = True, emptySectionCheck : bool = True, badReferenceCheck : bool = True):
        """
        Examines whole document and checks for mistakes. If a mistake occurred, it will be marked as annotation at appropriate place.
        Class variable mistakes_found indicates whether at least one mistake was marked.

        Args:
            annotatedPath (string): Path where annotated document will be stored.
            embeddedPdfAsImage (bool, optional): Determines if embedded PDFs inside document will be taken as images. Defaults to True.
            borderCheck (bool, optional): Determines if document will be scanned for any out of border content (overflow). Defaults to True.
            hyphenCheck (bool, optional): Determines if document will be scanned for wrong usage of hyphen. Defaults to True.
            imageWidthCheck (bool, optional): Determines if document will be scanned for images with width 85% to 99% of line width. Defaults to True.
            TOCCheck (bool, optional): Determines if document will be scanned for headings of level 3 or higher. Defaults to True.
            spaceBracketCheck (bool, optional): Determines if document will be scanned for missing space before any left bracket. Defaults to True.
            emptySectionCheck (bool, optional): Determines if document will be scanned for absence of text between (sub)section titles. Defaults to True.
            badReferenceCheck (bool, optional): Determines if document will be scanned for missing references (indicated by '??'). Defaults to True.
        """
        self.__resetCheckerVars()
        self.__embeddedPdfAsImage = embeddedPdfAsImage
        if borderCheck or hyphenCheck or imageWidthCheck or TOCCheck or spaceBracketCheck or emptySectionCheck or badReferenceCheck:
            findBorder = borderCheck or imageWidthCheck or emptySectionCheck
            if findBorder or emptySectionCheck:
                self.__getDocInfo(findBorder, emptySectionCheck)

            self.__resetCurrVars()
            for self.__currPage in self.__document:
                if borderCheck and not self.borderNotFound:
                    self.__overflowPageCheck()

                if hyphenCheck:
                    self.__hyphenPageCheck()

                if badReferenceCheck:
                    self.__doubleQuestionMarkPageCheck()

                if imageWidthCheck and not self.borderNotFound:
                    self.__imageWidthPageCheck()

                if TOCCheck:
                    self.__TOCSectionsCheck()

                if spaceBracketCheck:
                    self.__spaceBracketCheck()

                if emptySectionCheck:
                    if self.__currPage.number > 0:
                        self.__emptySectionCheck()
            
                self.__resetCurrVars()
        self.__document.save(annotatedPath)


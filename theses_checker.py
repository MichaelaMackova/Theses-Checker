#----------------------------------------------------------------------------
# File          : theses_checker.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Created Date  : 14.1.2023
# ---------------------------------------------------------------------------

import string
import random
from statistics import median
import fitz
import re
from enum import Enum


class Language(Enum):
    CZECH = 0
    SLOVAK = 1
    ENGLISH = 2
    

class Checker:
    RND_PAGE_CNT = 10
    HIGH_RED = (255, 128, 128)
    HIGHLIGHT_MARGIN = 1.5
    RED = (204, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, pdfPath : string, pdfLang : Language = None):
        self.mistakes_found = False
        self.borderNotFound = False
        self.__document = fitz.Document(pdfPath)
        self.__currPage = fitz.Page
        self.__currTextPage = fitz.TextPage
        self.__currPixmap = fitz.Pixmap
        self.__currDict = None
        self.__border = (-1.0, -1.0)
        self.__isContentPage = False
        self.__language = pdfLang
        self.__regularFont = None
        self.__isPreviousTitle = False
        


    def __rgbToPdf(self, color:tuple):
        return (color[0]/255.0, color[1]/255.0, color[2]/255.0)

    def __randomPagesIndex(self):
        docLen = len(self.__document)
        if docLen <= 5:
            return range(0, docLen)
        maxListLen = min(self.RND_PAGE_CNT, docLen-4)
        return random.sample(range(2, docLen-2), maxListLen)

    def __highlight(self, rects:list, color:tuple, text:string = None, title:string = None):
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
        for rect in overflow_rects:
            annot = self.__currPage.add_line_annot(fitz.Point(x,rect[1]-20), fitz.Point(x,rect[3]+20))
            annot.set_border(width=1)
            annot.set_colors(stroke=self.__rgbToPdf(self.RED))
            annot.update()



    def __getTextPage(self):
        if self.__currTextPage == None:
            self.__currTextPage = self.__currPage.get_textpage()



    def __getPageDictionary(self):
        if self.__currDict == None:
            self.__getTextPage()
            self.__currDict = self.__currPage.get_text("dict", textpage=self.__currTextPage, sort=True)



    def __getPageBorder(self):
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
        for i in range(len(fonts)):
            currFont = fonts[i]
            if not isinstance(currFont,dict):
                currFont = fonts[i][0]
            if ((currFont['name'] == font['name']) and (currFont['size'] == font['size']) and (currFont['flags'] == font['flags'])):
                return i
        return None

    

    def __getPageUsedFonts(self):
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
        index_mostUsedFont = 0
        for index in range(1,len(fonts)):
            if fonts[index][1] > fonts[index_mostUsedFont][1]:
                index_mostUsedFont = index
        return index_mostUsedFont

    

    def __getPageRegularFont(self):
        fonts = self.__getPageUsedFonts() 
        return fonts[self.__getMostUsedFontIndex(fonts)]

    

    def __getDocInfo(self, findBorder : bool, findRegularFont : bool):

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
                index = self.__getFontIndex(regularFonts, font[0])
                if index != None:
                    regularFonts[index] = (font[0], regularFonts[index][1] + font[1])
                else:
                    regularFonts.append(font)

            self.__resetCurrVars()

        if findBorder:
            borderLeft = median(left_borders)
            borderRight = median(right_borders)
            if borderLeft < borderRight:
                self.__border = (borderLeft, borderRight)
            else:
                # bad border found
                self.borderNotFound = True
                #TODO: skip checks where border is needed!!!
                pageBound = self.__document[0].rect
                self.__border = (pageBound[0], pageBound[2])

        if findRegularFont:
            self.__regularFont = regularFonts[self.__getMostUsedFontIndex(regularFonts)][0]



    def __getPixmap(self):
        if self.__currPixmap == None:
            self.__currPixmap = self.__currPage.get_pixmap()



    def __getPageRightOverflow(self):
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
                        overflow_rects.append([r_border+1,y-self.HIGHLIGHT_MARGIN,x+self.HIGHLIGHT_MARGIN,y+self.HIGHLIGHT_MARGIN])
                    else: 
                        # previous line had overflow -> merge rectanles
                        overflow_rects[-1][2] = max(overflow_rects[-1][2],x+self.HIGHLIGHT_MARGIN)
                        overflow_rects[-1][3] = y+self.HIGHLIGHT_MARGIN
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
                        overflow_rects.append([x-self.HIGHLIGHT_MARGIN,y-self.HIGHLIGHT_MARGIN,l_border,y+self.HIGHLIGHT_MARGIN])
                    else: 
                        # previous line had overflow -> merge rectanles
                        overflow_rects[-1][0] = min(overflow_rects[-1][0],x-self.HIGHLIGHT_MARGIN)
                        overflow_rects[-1][3] = y+self.HIGHLIGHT_MARGIN
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



    def __hyphenPageCheck(self):
        self.__getTextPage()
        rects = self.__currPage.search_for(" - ", textpage=self.__currTextPage)
        for rect in rects:
            self.mistakes_found = True
            self.__highlight(rect,self.HIGH_RED,"Pouzijte spojovnik (–) namisto pomlcky.", "Chyba")



    def __drawArrow(self,x_pointing:float,x:float,y:float):
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



    def __getBoolContentPage(self, pageFirstBlock : dict):
        if (pageFirstBlock['type'] == 0): 
            # --- text ---
            lines = pageFirstBlock['lines']
            if (len(lines) == 1):
                #contentText = "Obsah" if (self.__language == Language.CZECH or self.__language == Language.SLOVAK) else "Contents"
                if ( lines[0]['spans'][0]['text'] == "Obsah" or lines[0]['spans'][0]['text'] == "Contents"):
                    self.__isContentPage = True
                else:
                    self.__isContentPage = False



    def __TOCSectionsCheck(self):
        self.__getPageDictionary()
        blocks = self.__currDict['blocks']
        self.__getBoolContentPage(blocks[0])
        if (self.__isContentPage):
            for block in blocks:
                if block['type'] == 0: 
                    # --- text ---
                    lines = block['lines']
                    origin_y = -1.0
                    for line in lines:
                        line_origin = line['spans'][0]['origin']
                        if line_origin[1] != origin_y:
                            # new line, not tab -> section number
                            x = re.search("^\d+\.(?:\d+\.)+\d+", line['spans'][0]['text']) # example: 3.12.5
                            if x:
                                self.mistakes_found = True
                                self.__highlight([line['bbox']],self.HIGH_RED,"Nečíslovat nadpisy třetí a více úrovně", "Chyba")
                        origin_y = line_origin[1]



    def __deleteDuplicate(self, array : list):
        return list(dict.fromkeys(array))



    def __spaceBracketCheck(self):
        textBlocks = self.__currPage.get_text("blocks", flags=fitz.TEXT_PRESERVE_LIGATURES|fitz.TEXT_DEHYPHENATE|fitz.TEXT_MEDIABOX_CLIP)
        for block in textBlocks:
            if block[6] == 0:   # contains text
                text = block[4]
                if text[-1] == "\n":
                    text = text[:-1]
                
                text = text.replace("\n"," ")
                matchList = re.findall("\S\(", text)    # not " ("
                if matchList:
                    self.__getTextPage()
                    matchList = self.__deleteDuplicate(matchList)
                    for match in matchList:
                        rects = self.__currPage.search_for(match, textpage=self.__currTextPage)
                        for rect in rects:
                            self.mistakes_found = True
                            self.__highlight(rect,self.HIGH_RED,"Chybí mezera před levou závorkou.", "Chyba")



    def __isTitleBlock(self, blockNumber : int):
        block = self.__currDict['blocks'][blockNumber]
        block_info = dict(linesCount=0, fonts=[])
        if block['type'] == 0:
            # --- text ---
            lines = block['lines']
            block_info['linesCount'] = len(lines)
            origin_y = -1.0
            for line in lines:
                line_origin = line['spans'][0]['origin']
                if line_origin[1] == origin_y:
                    # not a new line
                    block_info['linesCount'] -= 1
                origin_y = line_origin[1]
                spans = line['spans']
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
                #TODO: delete
                #self.__highlight([block['bbox']],(220,255,255),str(block_info),"Nadpis")
                return True
                
        return False



    def __getBlockText(self, blockNumber : int):
        block = self.__currDict['blocks'][blockNumber]
        text = ""
        if block['type'] == 0:
            origin_y = -1.0
            origin_x = -1.0
            lines = block['lines']
            for line in lines:
                line_origin = line['spans'][0]['origin']
                if line_origin[1] == origin_y:
                    # not a new line
                    text = text[:-1] + "\t"
                else:
                    if line_origin[0] > origin_x and origin_x != -1.0:
                        # new paragraph
                        text = text[:-1] + "\n"
                origin_y = line_origin[1]
                origin_x = line_origin[0]
                spans = line['spans']
                for span in spans:
                    text += span['text']
                if text[-1] == "-":
                    text = text[:-1]
                else:
                    text+=" "
            text=text[:-1]
        return text



    def __emptySectionCheck(self):
        isPreviousNewChapter=False
        self.__getPageDictionary()
        blocks = self.__currDict['blocks']
        for blockNumber in range(len(blocks)):
            if self.__isTitleBlock(blockNumber):
                blockText = self.__getBlockText(blockNumber)
                x = re.search("\t\d+$", blockText) # example: Úvod   2
                if self.__isPreviousTitle and not isPreviousNewChapter and not x:
                    y1=blocks[blockNumber-1]['bbox'][3]
                    y2=blocks[blockNumber]['bbox'][1]
                    if y1 < y2:
                        rect = fitz.Rect(self.__border[0],y1,self.__border[1],y2)
                        self.mistakes_found = True
                        self.__highlight([rect],self.HIGH_RED,"Chybí text mezi nadpisy","Chyba")
                x = re.search("^(?:Kapitola|Chapter) \d+$", blockText) # example: Kapitola 4; Chapter 4
                if  x:
                    isPreviousNewChapter = True
                else:
                    isPreviousNewChapter = False
                self.__isPreviousTitle = True
            else:
                isPreviousNewChapter = False
                self.__isPreviousTitle = False



    def __resetCurrVars(self):
        self.__currPage = None
        self.__currDict = None
        self.__currPixmap = None
        self.__currTextPage = None


    def annotate(self ,annotatedPath : string, borderCheck : bool = True, hyphenCheck : bool = True, imageWidthCheck : bool = True, TOCCheck : bool = True, spaceBracketCheck : bool = True, emptySectionCheck : bool = True):
        self.__resetCurrVars()
        if borderCheck or hyphenCheck or imageWidthCheck or TOCCheck or spaceBracketCheck or emptySectionCheck:
            findBorder = borderCheck or imageWidthCheck or emptySectionCheck
            if findBorder or emptySectionCheck:
                self.__getDocInfo(findBorder, emptySectionCheck)

            self.__resetCurrVars()

            for self.__currPage in self.__document:
                if borderCheck:
                    self.__overflowPageCheck()

                if hyphenCheck:
                    self.__hyphenPageCheck()

                if imageWidthCheck:
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


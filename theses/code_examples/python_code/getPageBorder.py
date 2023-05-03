def getPageBorder(currPage):
    potentialLeft = []
    potentialRight = []

    for line in currPage.lines:
        if not firstLine(line):
            potentialLeft.add(line.border.x0)
        
        if not lastLine(line):
            potentialRight.add(line.border.x1)

    xLeft = median(potentialLeft)
    xRight = median(potentialRight)
    return (xLeft, xRight)
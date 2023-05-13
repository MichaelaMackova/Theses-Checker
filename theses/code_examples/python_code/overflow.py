def getOverflow(currPage):
    overflowList = []
    pageBorder = getPageBorder()
    pagePicture = getPageAsPicture(currPage)
    for lineOfPixels in pagePicture:
        for i in range(0, len(lineOfPixels)):
            pixel = lineOfPixels[i]
            if (not outOfBounds(pixel.coordinates, pageBorder)):
                break
            if (pixel.color != currPage.baseColor):
                overflowList.add((pixel.x,pixel.y,pageBorder.x0,pixel.y))

        for i in range(len(lineOfPixels), 0, -1):
            pixel = lineOfPixels[i]
            if (not outOfBounds(pixel.coordinates, pageBorder)):
                break
            if (pixel.color != currPage.baseColor):
                overflowList.add((pageBorder.x1,pixel.y,pixel.x,pixel.y))

    return overflowList
def getOverflow(currPage):
    overflowList = []
    pageBorder = getPageBorder()
    pagePicture = getPageAsPicture(currPage)
    for lineOfPixels in pagePicture:
        for pixel in lineOfPixels:
            if (outOfBounds(pixel.coordinates, pageBorder)
                    and (pixel.color != currPage.baseColor)):
                overflowList.add(pixel)

    return overflowList
docInfo = getDocInfo()

for currentPage in document:
    if check1:
        Check1(currentPage, docInfo)
    
    if check2:
        Check2(currentPage, docInfo)

    # ...

document.save(outPath)
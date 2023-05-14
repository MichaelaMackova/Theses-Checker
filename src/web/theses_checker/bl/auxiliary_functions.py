import uuid
import os

def generateUniqueFileName(pdfDir : str, pdfPrefix : str|None, fileType : str):
    """
        generates unique filename in pdfDir directory as: pdfPrefix-uniqueId.fileType

        if pdfPrefix is None or empty string unique filename is: uniqueId.fileType
    """
    
    if pdfPrefix == None:
        pdfPrefix = ''
    if pdfPrefix != '':
        pdfPrefix = pdfPrefix + '-'

    fileName = ''
    while True:
        fileName = pdfPrefix + uuid.uuid4().hex + '.' + fileType
        annotated_path = os.path.join(pdfDir, fileName)
        if not os.path.exists(annotated_path):
            break
    return fileName
#----------------------------------------------------------------------------
# File          : auxiliary_functions.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Last Updated  : 25.11.2024
# License       : AGPL-3.0 license
# ---------------------------------------------------------------------------

def generateUniqueFileName(pdfDir : str, pdfPrefix : str|None, fileType : str):
    """
        Generates unique filename in pdfDir directory as: "pdfPrefix-uniqueId.fileType"

        if pdfPrefix is None or empty string, unique filename is: "uniqueId.fileType"

        Args:
            pdfDir (str): directory where the file is checked for uniqueness
            pdfPrefix (str|None): prefix of the generated filename (usually name of the file without extension)
            fileType (str): extension of the generated filename
    """
    import uuid
    import os
    
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

def saveDictAsJSON(dict : dict, path : str):
    """
        Saves dictionary as JSON file

        Args:
            dict (dict): dictionary to be saved
            path (str): path to the JSON file
    """
    import json

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dict, f, indent=4, ensure_ascii=False)

def readJSONAsDict(path : str) -> dict:
    """
        Reads JSON file as dictionary

        Args:
            path (str): path to the JSON file
    """
    import json

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

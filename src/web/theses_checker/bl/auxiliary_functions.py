#----------------------------------------------------------------------------
# File          : auxiliary_functions.py
# Created By    : Michaela Macková
# Login         : xmacko13
# Email         : michaela.mackovaa@gmail.com
# Last Updated  : 03.12.2024
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
    
def checkStorageAvailableSpace(file_size : int) -> bool:
    """
        Checks if there is enough storage space for a file with size file_size

        Args:
            file_size (int): size of the file in bytes
    
        Returns:
            bool: True if there is enough storage space, False otherwise
    """
    import subprocess
    import os
    from django.conf import settings

    if settings.OPERATING_SYSTEM == 'Windows':
        script_path = '\"' + os.path.join(settings.BASE_DIR, 'getStorageAvailableSpace.ps1') + '\"' # path with spaces
        available_storage = int(subprocess.check_output(['powershell', '& ' + script_path]).decode('utf-8').strip())
    elif settings.OPERATING_SYSTEM == 'Linux':
        if settings.MAX_STORAGE_SPACE != None:
            bash_path = os.path.join(settings.BASE_DIR, 'getStorageUsage.sh')
            available_storage = settings.MAX_STORAGE_SPACE - int(subprocess.check_output(['bash', bash_path]).decode('utf-8').strip())
        else:
            bash_path = os.path.join(settings.BASE_DIR, 'getStorageAvailableSpace.sh')
            available_storage = int(subprocess.check_output(['bash', bash_path]).decode('utf-8').strip())
    else:
        raise ValueError("Invalid operating system")

    return available_storage >= file_size

def deleteFilesOlderThanPeriod():
    """
        Deletes files using periodicDeleteFiles.sh script (on Linux) or periodicDeleteFiles.ps1 script (on Windows)
    """
    import os
    import subprocess
    from django.conf import settings

    if settings.OPERATING_SYSTEM == 'Windows':
        script_path = '\"' + os.path.join(settings.BASE_DIR, 'periodicDeleteFiles.ps1') + '\"' # path with spaces
        subprocess.check_call(['powershell', '& ' + script_path])

    elif settings.OPERATING_SYSTEM == 'Linux':
        script_path = os.path.join(settings.BASE_DIR, 'periodicDeleteFiles.sh')
        subprocess.check_call(['bash', script_path])

    else:
        raise ValueError("Invalid operating system")

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
    
def checkStorageAvailableSpace(file_size : int, max_storage_space : int|None = None) -> bool:
    """
        Checks if there is enough storage space for a file with size file_size

        Args:
            file_size (int): size of the file in bytes
            max_storage_space (int|None, optional): maximum storage space in bytes, if None, maximum storage space is determined by the system (default None)
            os_win (bool, optional): if True, the function is called on Windows, otherwise on Linux (default False)
    
        Returns:
            bool: True if there is enough storage space, False otherwise
    """
    import subprocess
    import os
    from django.conf import settings

    #TODO: implement for Windows (přidat settins.OS)

    if max_storage_space != None:
        bash_path = "./getStorageUsage.sh"
        # bash_path = os.path.join(settings.BASE_DIR, 'getStorageUsage.sh')
        available_storage = max_storage_space - int(subprocess.check_output(['bash', bash_path]).decode('utf-8').strip())
    else:
        bash_path = "./getStorageAvailableSpace.sh"
        # bash_path = os.path.join(settings.BASE_DIR, 'getStorageAvailableSpace.sh')
        available_storage = int(subprocess.check_output(['bash', bash_path]).decode('utf-8').strip())

    return available_storage >= file_size

def callBashScript(script_path : str):
    """
        Calls bash script

        Args:
            script_path (str): path to the bash script
    """
    import subprocess

    #TODO: implement for Windows (přidat settins.OS)

    subprocess.check_call(['bash', script_path])

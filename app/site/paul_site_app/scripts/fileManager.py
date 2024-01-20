from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent))

from resource.info import site
import os
from datetime import datetime



def structure():
    context = {
        "fileList": []
    }
    for root, foldersWithinSubFolder, files in os.walk(site.FILES, topdown=True):
        for file in files:
            if os.path.isfile(os.path.join(root, file)):
                fileStat = os.stat(os.path.join(root, file))
                fileInfo = {
                    "name": file,
                    "path": f'/files/{os.path.join(root, file).replace(site.FILES, "")[1:]}',
                    "relPath": f'./{os.path.split(os.path.join(root, file))[0].replace(site.FILES, "")[1:]}' if (len(os.path.split(os.path.join(root, file))[0].replace(site.FILES, "")[1:]) != 0) else ("."),
                    "size": f'{str(fileStat.st_size)} bytes' if (fileStat.st_size < 1024) else (f'{str(round(fileStat.st_size/1024, 2))} kilobytes' if (fileStat.st_size < 1024 ** 2) else (f'{str(round(fileStat.st_size/(1024**2), 2))} megabytes' if (fileStat.st_size < 1024 ** 3) else (f'{str(round(fileStat.st_size/(1024**3), 2))} gigabytes' if (fileStat.st_size < 1024 ** 4) else ("N/A")))),
                    "creationDate": f"{datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%m/%d/%Y')} @ {str(int(datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%H')) - 12) if (int(datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%H')) > 12) else (str(int(datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%H'))))}:{datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%M:%S')} {'PM' if (int(datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%H')) > 12) else ('AM')}"
                }
                context["fileList"].append(fileInfo)
    return context

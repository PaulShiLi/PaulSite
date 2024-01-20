from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

from resource.info import site, ENV
import os

DO_NOT_DELETE = ENV["site"]["files"]["do_not_delete"]

def structure(dictReturn: bool = True, safe: bool = False):
    context = {}
    for root, foldersWithinSubFolder, files in os.walk(site.FILES, topdown=True):
        for file in files:
            if os.path.isfile(os.path.join(root, file)):
                filePath = f'/files/{os.path.join(root, file).replace(site.FILES, "")[1:]}'
                relPath = f'./{os.path.split(os.path.join(root, file))[0].replace(site.FILES, "")[1:]}' if (len(os.path.split(os.path.join(root, file))[0].replace(site.FILES, "")[1:]) != 0) else (".")
                fileStat = os.stat(os.path.join(root, file))
                fileSize = f'{str(fileStat.st_size)} bytes' if (fileStat.st_size < 1024) else (f'{str(round(fileStat.st_size/1024, 2))} kilobytes' if (fileStat.st_size < 1024 ** 2) else (f'{str(round(fileStat.st_size/(1024**2), 2))} megabytes' if (fileStat.st_size < 1024 ** 3) else (f'{str(round(fileStat.st_size/(1024**3), 2))} gigabytes' if (fileStat.st_size < 1024 ** 4) else ("N/A"))))
                if dictReturn == True:
                    fileInfo = {
                        filePath: {
                            "name": file,
                            "path": filePath,
                            "relPath": relPath,
                            "fileSize": fileSize
                            },
                    }
                else:
                    baseName = f"{file} | {relPath}"
                    fileName = baseName if len(baseName) < 100 else f"{file[:len(baseName) - 103]}... | {relPath}"
                    fileInfo = {
                        fileName : f"{relPath[2:]}/{file}"
                    }
                context.update(fileInfo) if safe == False else (context.update(fileInfo) if os.path.join(root, file) not in [os.path.join(site.FILES, dnd[2:]) for dnd in DO_NOT_DELETE] else None)

    return context

def folder(ignoreBase: bool = False):
    if not ignoreBase:
        return {x[0].replace(site.FILES, "."): x[0].replace(site.FILES, "")[1:] for x in os.walk(site.FILES)}
    else:
        returnDict = {}
        for x in os.walk(site.FILES):
            if x[0] != site.FILES:
                returnDict.update({x[0].replace(site.FILES, "."): x[0].replace(site.FILES, "")[1:]})
        return returnDict

class DisplayablePath(object):
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(list(path
                               for path in root.iterdir()
                               if criteria(path)),
                          key=lambda s: str(s).lower())
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(path,
                                         parent=displayable_root,
                                         is_last=is_last,
                                         criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls, path):
        return True

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))

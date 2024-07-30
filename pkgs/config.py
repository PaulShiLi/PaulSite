from pathlib import Path
import os
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from dataclasses import dataclass
import orjson


@dataclass
class File:
    """File type for files"""

    name: str
    path: str

    @property
    def content(self) -> dict | str | list:
        """Content of the file

        Returns:
            dict | str | list: Content of the file
        """
        content: dict | str | list | None = None

        if not os.path.exists(self.path):
            return None

        with open(self.path) as file:
            content = file.read()
            try:
                content = orjson.loads(content)
            except:
                pass
        return content

    @property
    def extension(self) -> str | None:
        """Extension of the file

        Returns:
            str | None: Extension of the file if it exists else None
        """
        if "." in self.path:
            return self.path.split(".")[-1]
        else:
            return None


class Dirs:
    ROOT: Path = Path(__file__).parent.parent
    ASSETS: Path = Path(__file__).parent.parent / "assets"
    FILES: Path = Path(__file__).parent.parent / "files"
    STATIC: Path = Path(__file__).parent.parent / "assets" / "static"

class Files:
    ENV: File = File(
        "env.json",
        os.path.join(Dirs.ROOT, "env.json")
    )

    REQUIREMENTS: File = File(
        "requirements.txt",
        os.path.join(Dirs.ROOT, "requirements.txt")
    )

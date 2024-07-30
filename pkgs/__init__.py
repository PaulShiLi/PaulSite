import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pkgs.config import Files, Dirs

ENV = Files.ENV
BASE_DIR = Dirs.ROOT
ASSETS_DIR = Dirs.ASSETS

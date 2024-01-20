from pathlib import Path
import os
import json

with open(os.path.join(Path(__file__).resolve().parent.parent, 'env.json'), 'r') as f:
    ENV = json.load(f)

class PATH:
    PARENT_DIR = os.path.join(Path(__file__).resolve().parent.parent)
    ENV = os.path.join(Path(__file__).resolve().parent.parent, 'env.json')
    SPOTIFY_AUTH = os.path.join(Path(__file__).resolve().parent.parent, 'spotify_auth.json')
    VENV = os.path.join(Path(__file__).resolve().parent.parent, 'site_env')
    class API:
        api = os.path.join(Path(__file__).resolve().parent.parent, 'assets', 'static', 'api', 'api.json')
        class SPOTIFY:
            STATUS = os.path.join(Path(__file__).resolve().parent.parent, 'assets', 'static', 'api', 'spotify', 'status.json')
            HISTORY = os.path.join(Path(__file__).resolve().parent.parent, 'assets', 'static', 'api', 'spotify', 'history.json')
        class DISCORD:
            STATUS = os.path.join(Path(__file__).resolve().parent.parent, 'assets', 'static', 'api', 'discord', 'status.json')

class pkgs:
    class SPOTIFY:
        FOLDER = os.path.join(Path(__file__).resolve().parent.parent, 'pkgs', 'spotify')
    
    class DISCORD:
        FOLDER = os.path.join(Path(__file__).resolve().parent.parent, 'pkgs', 'discord')
    
    class NODE:
        FOLDER = os.path.join(Path(__file__).resolve().parent.parent, 'pkgs', 'nodeModules')

class site:
    BASE = os.path.join(Path(__file__).resolve().parent.parent, 'app')
    FILES = os.path.join(Path(__file__).resolve().parent.parent, 'files')
    ASSETS = os.path.join(Path(__file__).resolve().parent.parent, 'assets')
    STATIC = os.path.join(Path(__file__).resolve().parent.parent, 'assets', 'static')
    TEMPLATES = os.path.join(Path(__file__).resolve().parent.parent, 'assets', 'templates')
    SITE = os.path.join(Path(__file__).resolve().parent.parent, 'app', 'site')
    
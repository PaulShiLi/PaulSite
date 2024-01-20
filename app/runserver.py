from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent))

import subprocess
import json
from resource.info import ENV, site

class start:
    
    def __init__(self, selection: str = "discord", args: list = []) -> None:
        self.config = ENV
        self.selectFuncs = {
            "discord": self.discord,
            "site": self.site
        }
        print(f"Starting {self.selectFuncs[selection]} ...\n")
        self.selectFuncs[selection](args)
    
    def discord(self, args: list = []):
        self.proc = subprocess.Popen(
            f'python3 {os.path.join(Path(__file__).resolve().parent, "discordBot", "manager.py")}',
            shell=True
        )

    def site(self, args: list = []):
        # Use uvicorn to host http server
        self.proc = subprocess.Popen(
            f"""{
            f'{";".join(args)};' if len(args) != 0 else ""}
            uvicorn paul_site.asgi:application --reload 
            --host {self.config["site"]['http']["ADDRESS"]} 
            --port {self.config["site"]['http']["PORT"]}
            """.replace("\n", " "),
            shell=True
        )

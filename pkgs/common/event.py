import colorama
import datetime
import os
from typing import Literal

def post(toPrint: str, evtType: Literal["loop", "bot", "warn", "error"], filePath: str):
    evts = {
        "loop": colorama.Fore.CYAN,
        "error": colorama.Fore.RED,
        "warn": colorama.Fore.YELLOW,
        "bot": colorama.Fore.MAGENTA
    }
    file = filePath.split(os.sep)[-1].replace(".py", "")
    parentDir = filePath.split(os.sep)[-2]
    print(
        f"""{evts[evtType]}{colorama.Style.BRIGHT}[{evtType.upper()}: {parentDir}/{file}]{colorama.Style.RESET_ALL} {colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}@ {datetime.datetime.now()}{colorama.Style.RESET_ALL}{evts[evtType]}{colorama.Style.BRIGHT}:{colorama.Style.RESET_ALL}\n{toPrint}"""
    )

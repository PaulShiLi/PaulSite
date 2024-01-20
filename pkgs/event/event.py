import colorama
import datetime
import os

def post(toPrint: str, evtType: str, filePath: str):
    evts = {
        "loop": colorama.Fore.CYAN,
        "error": colorama.Fore.RED,
        "bot": colorama.Fore.MAGENTA,
        "info": colorama.Fore.BLUE,
    }
    file = filePath.split(os.sep)[-1].replace(".py", "")
    parentDir = filePath.split(os.sep)[-2]
    print(
        f"""{evts[evtType]}{colorama.Style.BRIGHT}[{evtType.upper()}: {parentDir}/{file}]{colorama.Style.RESET_ALL} {colorama.Fore.LIGHTBLUE_EX}{colorama.Style.BRIGHT}@ {datetime.datetime.now()}{colorama.Style.RESET_ALL}{evts[evtType]}{colorama.Style.BRIGHT}:{colorama.Style.RESET_ALL}\n{toPrint}"""
    )

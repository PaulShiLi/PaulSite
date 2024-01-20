import os
from pathlib import Path
import argparse
from app import runserver

from resource.info import PATH, site, pkgs

class parse:
    def read(args):
        argList = [str(args.read[n]) for n in len(args)]
        return argList

    def argSetup():
        # Create Parser Object
        parser = argparse.ArgumentParser(
            prog="Paul's site",
            description="A website and discord bot starter Paul's site",
            epilog="Made by Paul"
        )

        # Defining arguments for the parser object
        parser.add_argument("-s", "--site", help="Starts the website", action='store_true')
        parser.add_argument("-d", "--discord", help="Starts the discord bot", action='store_true')
        parser.add_argument("-b", "--build", help="Builds files like markdowns", action='store_true')
        parser.add_argument("-e", "--env", help="Include custom env path", type=str, default=PATH.VENV)
        # parse the arguments from standard input
        args = parser.parse_args()
        envCommand = f"source {os.path.join(args.env, 'bin', 'activate')}"
        commands = [
            envCommand,
            f"cd {pkgs.NODE.FOLDER}",
            "npm run tailwind-build",
            f"cd {site.SITE}"
        ]
        if args.site == True:
            # Kill the process running on port 8000
            runserver.start(selection="site", args=commands)
        elif args.discord == True:
            runserver.start(selection="discord")
        elif args.build == True:
            print("Building files...")
        else:
            runserver.start(selection="site", args=commands)


if __name__ == '__main__':
    parse.argSetup()
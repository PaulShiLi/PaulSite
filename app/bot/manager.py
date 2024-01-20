# Manager-san base code
from pathlib import Path
import os
import sys

sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent))

from resource.info import ENV, PATH
from pkgs.event import event

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import asyncio
from app.bot.scripts import embed
import importlib.util

intents = nextcord.Intents.all()
intents.members = True
intents.presences = True
intents.message_content = True
intents.messages = True

# Updates my discord user presence and status every 2 seconds and saves it to info.json for the site


class onLoad:
    tasks = []

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    async def setLoop(self):
        loops = []
        for data in os.walk(
            os.path.join(Path(__file__).resolve().parent, "loops"), topdown=False
        ):
            dirName, subDir, files = data
            for filename in files:
                if filename.endswith(".py"):
                    loops.append((filename[:-3], dirName))

        for loop in loops:
            modName, modDir = loop
            moduleSpec = importlib.util.spec_from_file_location(
                modName, os.path.join(modDir, f"{modName}.py")
            )
            module = importlib.util.module_from_spec(moduleSpec)
            moduleSpec.loader.exec_module(module)
            asyncio.create_task(module.run(self.client))

            event.post(
                toPrint=f"{loop[0].title()} loop started",
                evtType="bot",
                filePath=os.path.join(modDir, f"{modName}.py"),
            )

    async def runTasks(self):
        self.status = await asyncio.create_task(self.setLoop())


class Manager(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=ENV["discord"]["guild"]["prefix"], intents=intents
        )
        self.loadCogs()
        self.onLoad = onLoad(self)

    async def on_ready(self):
        await self.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.listening,
                name="your website",
                url="https://psli.space",
            ),
            status=nextcord.Status.online,
        )
        event.post(
            toPrint="Manager-san connected to Discord", evtType="bot", filePath=__file__
        )
        await self.get_channel(ENV["discord"]["guild"]["channels"]["logs"]).send(
            embed=embed.createEmbed(
                title="Manager-san",
                description="Manager-san koko wa desu!",
                timestampFooter=True,
            )
        )
        # Starts running tasks
        await self.onLoad.runTasks()

    def loadCogs(self):
        initial_extensions = []
        for filename in os.listdir(
            os.path.join(Path(__file__).resolve().parent, "cogs")
        ):
            if filename.endswith(".py"):
                initial_extensions.append(f"app.bot.cogs.{filename[:-3]}")
        event.post(toPrint="Loading Cogs...", evtType="bot", filePath=__file__)
        for extension in initial_extensions:
            event.post(
                toPrint=f"Loading extension {extension}",
                evtType="bot",
                filePath=__file__,
            )
            try:
                self.load_extension(extension)
                event.post(
                    toPrint=f"{extension} loaded", evtType="bot", filePath=__file__
                )
            except Exception as e:
                event.post(
                    toPrint=f"Failed to load {extension}:\nError: {e}",
                    evtType="error",
                    filePath=__file__,
                )


manager = Manager()
manager.run(ENV["discord"]["TOKEN"])

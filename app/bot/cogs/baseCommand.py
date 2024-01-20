# Base import
from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

from resource.info import ENV
from app.bot.scripts import embed
from pkgs.wrappers.discordWrapper import Console

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import asyncio
import nest_asyncio


nest_asyncio.apply()

shutdown_event = asyncio.Event()

class baseCommand(commands.Cog):
    proc = None

    def __init__(self, client: commands.Bot):
        self.client = client
        self.console = Console(self.client)

    @nextcord.slash_command()
    async def bot(self, interaction: Interaction):
        pass

    @bot.subcommand(description="Shuts down Site Manager!")
    async def shutdown(self, interaction: Interaction):
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title="Exit",
                description="Site Manager shuts down successfully!",
                footer=f"Requested by {interaction.user.name}"
            )
        )
        self.console.log(
            f"Site Manager shuts down successfully!\nRequested by {interaction.user.name}",
            title="Shutdown"
        )
        exit()


def setup(client):
    client.add_cog(baseCommand(client))

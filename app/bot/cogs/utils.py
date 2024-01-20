from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent))

from app.bot.scripts import embed
from resource.info import ENV

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import asyncio

class utils(commands.Cog):
    
    def __init__(self, client: commands.Bot):
        self.client = client
    
    @nextcord.slash_command(name="clear",
                            description="Deletes messages from a channel")
    async def clear(self,
                    interaction: Interaction,
                    channel: nextcord.TextChannel = SlashOption(required=True),
                    amount: int = SlashOption(required=True, description="Amount of messages to clear")
                    ):
        await interaction.response.defer()
        await channel.purge(limit=amount, bulk=True)
        try:
            await interaction.followup.send(
                embed=embed.createEmbed(
                    title=f"Cleared {amount} messages",
                    description=f"Cleared `{amount}` messages from <#{channel.id}>"
                )
            )
        except nextcord.errors.NotFound:
            await interaction.channel.send(
                embed=embed.createEmbed(
                    title=f"Cleared {amount} messages",
                    description=f"<@{interaction.user.id}>\nCleared `{amount}` messages from <#{channel.id}>"
                )
            )

def setup(client):
    client.add_cog(utils(client))
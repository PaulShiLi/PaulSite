from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent))

from app.bot.scripts import embed

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import asyncio


class getData(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command()
    async def get(self, interaction: Interaction):
        pass

    @get.subcommand(description="Gets the server ID")
    async def guild(self, interaction: Interaction):
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title="Get Guild ID",
                description=f"Guild ID: {interaction.guild_id}",
                footer=f"Requested by {interaction.user.name}"
            )
        )

    @get.subcommand(description="Gets the channel ID")
    async def channel(
        self,
        interaction: Interaction,
        channel: nextcord.TextChannel = SlashOption(required=True)
    ):
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title="Get Channel ID",
                description=f"Channel ID: {channel.id}",
                footer=f"Requested by {interaction.user.name}"
            )
        )

    @get.subcommand(description="Gets the user ID")
    async def user(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(required=True)
    ):
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title="Get User ID",
                description=f"User ID: {user.id}",
                footer=f"Requested by {interaction.user.name}"
            )
        )

    @get.subcommand(description="Gets the user's image link")
    async def pfp(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(required=True)
    ):
        guild = self.client.get_guild(interaction.guild.id)
        member = guild.get_member(user.id)
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title="Get User Image",
                description=f"User Image: {member.avatar.url}",
                footer=f"Requested by {interaction.user.name}"
            )
        )

    @get.subcommand(description="Gets the user's presence")
    async def status(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(required=True)
    ):
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title="Get User Status",
                description=f"User Status: {user.activities}",
                footer=f"Requested by {interaction.user.name}"
            )
        )

def setup(client):
    client.add_cog(getData(client))

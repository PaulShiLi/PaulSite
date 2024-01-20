from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

from resource.info import PATH, ENV
from app.bot.scripts import embed
from textwrap import dedent

from nextcord.ext import commands
from nextcord.guild import GuildChannel

class Console:
    
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
    
    async def error(self, *args, title: str = None, file: str = None):
        channel = self.client.get_guild(ENV['discord']['guild']['id']).get_channel(ENV['discord']['guild']['channels']['errorLog'])
        await channel.send(embed=embed.createEmbed(
            title=f"😭 Error{'- ' + title if title != None else ''}",
            description=dedent(
                f"""
                {' '.join(args)}
                """
            ),
            timestampFooter=True,
            color=embed.Color.RED
        ))
    
    async def log(self, title: str = None, *args):
        channel = self.client.get_guild(ENV['discord']['guild']['id']).get_channel(ENV['discord']['guild']['channels']['logs'])
        await channel.send(embed=embed.createEmbed(
            title=f"📝 Log{'- ' + title if title != None else ''}",
            description=dedent(
                f"""
                {' '.join(args)}
                """
            ),
            timestampFooter=True,
            color=embed.Color.BLUE
        ))
    
    async def alert(self, title: str = None, *args):
        channel = self.client.get_guild(ENV['discord']['guild']['id']).get_channel(ENV['discord']['guild']['channels']['alerts'])
        await channel.send(embed=embed.createEmbed(
            title=f"🔔 Alert{'- ' + title if title != None else ''}",
            description=dedent(
                f"""
                <@{ENV['discord']['roles']['alerts']}>
                
                {' '.join(args)}
                """
            ),
            timestampFooter=True,
            color=embed.Color.yellow
        ))
    
    async def send(self, channel: GuildChannel, title: str = None, *args):
        channel = self.client.get_guild(ENV['discord']['guild']['id']).get_channel(channel)
        await channel.send(embed=embed.createEmbed(
            title=f"📝 Log{'- ' + title if title != None else ''}",
            description=dedent(
                f"""
                {' '.join(args)}
                """
            ),
            timestampFooter=True,
            color=embed.Color.BLUE
        ))
from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

from resource.info import ENV

import nextcord
import datetime

THUMBNAIL = ENV["discord"]["IMG"]

class Color(nextcord.Color):
    STANDARD = nextcord.Color.from_rgb(148, 167, 189)
    BLUE = nextcord.Color.from_rgb(122, 162, 247)
    CYAN = nextcord.Color.from_rgb(0, 255, 255)
    RED = nextcord.Color.from_rgb(116, 6, 23)

def createEmbed(title=None, description=None, fields: list = [], inline: bool = True, thumbnail: str = None, footer: str = None, timestampFooter: bool = True, url: str = None, image: str = None, color: nextcord.Color = Color.STANDARD):
    embed = None
    if title != None and description != None:
        embed = nextcord.Embed(
            title=title,
            description=description,
            color=color,
        )
    elif title != None and description == None:
        embed = nextcord.Embed(
            title=title,
            color=color
        )
    elif title == None and description != None:
        embed = nextcord.Embed(
            description=description,
            color=color
        )
    else:
        embed = nextcord.Embed(
            color=color
        )
    if url != None:
        embed.url = url
    author = THUMBNAIL
    if thumbnail == None:
        author = None
        thumbnail = THUMBNAIL
        embed.set_thumbnail(url=THUMBNAIL)
        # embed.set_author(name="Manager-san")
    else:
        embed.set_thumbnail(url=thumbnail)
        # embed.set_author(name="Manager-san", icon_url=author)
        embed.set_author(icon_url=author)
    if footer != None:
        embed.set_footer(text=footer)
    for name, value in fields:
        if name != None and value != None:
            embed.add_field(name=name, value=value, inline=inline)
        elif name != None and value == None:
            embed.add_field(name=name, inline=inline)
        elif name == None and value != None:
            embed.add_field(value=value, inline=inline)
    if image != None:
        embed.set_image(image)
    if timestampFooter == True:
        embed.timestamp = datetime.datetime.now()
    return embed

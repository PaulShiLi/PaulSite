from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

from pkgs import ENV
from pkgs.common import event
from pkgs.mongo.db import Mongo, mongoClient
from pkgs.spotify.spotify import spotifyDb
from app.bot.scripts import embed

import aiohttp
import aiofiles
import asyncio
import json
import nextcord
from nextcord.ext import commands
from textwrap import dedent
import time
from urllib.parse import quote_plus

ENV = ENV.content
spClient = spotifyDb()

curTime = 0

# Update every 2 seconds
async def delay():
    await asyncio.sleep(2)

class handler:
    
    async def getUserStatus(client: commands.Bot):
        guild = client.get_guild(ENV['discord']['guild']['id'])
        member = guild.get_member(ENV['discord']['USER_ID'])
        
        isEmpty = True if len(Mongo.find("discord", "status")) == 0 else False
        
        if "status" in mongoClient["discord"].list_collection_names() and not isEmpty:
            customActivity = Mongo.find("discord", "status")[0]["custom"]
        else:
            customActivity = ""
        # Mongo.delete("discord", "status")
        #     Mongo.insert(
        #         "discord",
        #         "status",
        #         {
        #             "status": member.status.name,
        #             "custom": ""
        #         }
        #     )
                
        if len(member.activities) != 0:
            for acti in member.activities:
                if acti.type == nextcord.ActivityType.custom:
                    acti = acti.to_dict()
                    if (acti.type == 4):
                        try:
                            customActivity = f"{acti['emoji']['name']} {acti['state']}"
                        except KeyError:
                            customActivity =  f"{acti['state']}"
                if acti.type == nextcord.ActivityType.playing:
                    customActivity = f"Playing {acti.details} {acti.state}"
                    # Upload to now playing
                    if acti.name == "Apple Music":
                        image = acti.assets["large_image"]
                        if "http" in image:
                            imgLink = f"http{image.split('http')[-1]}".replace("http/", "http://").replace("https/", "https://")
                        else:
                            imgLink = "https://www.apple.com/newsroom/images/product/apple-music/apple_music-update_hero_08242021.jpg.news_app_ed.jpg"
                        
                        # Check if there is a song already playing in the database and if so check if there's a duration and if not continue to update the song
                        songUpdate = {
                            "_id": 0,
                            "name": acti.details,
                            "artist": acti.state[3:] if acti.state.startswith("by ") else acti.state,
                            "artistLink": "",
                            "link": f"https://music.youtube.com/search?q={quote_plus(acti.details + ' ' + acti.state[3:] if acti.state.startswith('by ') else acti.state)}",
                            "pic": imgLink,
                            "releaseDate": "",
                            "status": "currentSong",
                            "end": acti.end.timestamp(),
                            "platform": acti.name
                        }
                        if acti.name == spClient.recentlyPlayed("current")[0]["platform"] or spClient.recentlyPlayed("current")[0]["status"] == "noCurrentSong":
                            # print(f"Song Update: {songUpdate}")
                            Mongo.replace("spotify", "current", {"_id": 0}, songUpdate)
                else:
                    recentPlayed = spClient.recentlyPlayed("current")[0]
                    if recentPlayed["status"] == "currentSong" and recentPlayed["platform"] == "Apple Music" and recentPlayed["end"] <= time.time():
                        spClient.updateDb("current")
        else:
            customActivity = ""
            try:
                spClient.updateDb("current")
            except IndexError:
                asyncio.sleep(1)
                spClient.updateDb("current")                

        toUpdate = {
            '_id': 0,
            'status': member.status.name,
            'custom': customActivity
        }
        
        api = Mongo.find("discord", "status")
        
        if len(api) == 0:
            api = {}
        else:
            api = api[0]
        
        # print(f"""
        #       To update: {toUpdate}
        #       API: {api}
        #       Compare: {api != toUpdate}
        #       """)
        
        if (api != toUpdate):
            api = toUpdate
            if ENV["site"]["apiPost"] != True:
                if "status" in mongoClient["discord"].list_collection_names() and not isEmpty:
                    Mongo.replace("discord", "status", {
                        "_id": 0}, toUpdate)
                else:
                    Mongo.insert("discord", "status", toUpdate)
            else:
                async with aiohttp.ClientSession() as session:
                    payload = {
                        "content": api["discord"]["status"],
                        "auth": {
                            "username": ENV["django"]["api"]["username"],
                            "passwd": ENV["django"]["api"]["passwd"]
                        }
                    }
                    async with session.post(
                        f"{ENV['site']['siteAddress']}/api/discord/status",
                        json=payload
                        ) as resp:
                        print(await resp.text())
                    del payload
            event.post(
                toPrint= "Discord Json API files updated",
                evtType= "bot",
                filePath= __file__
            )
                    
 
 
async def run(client: commands.Bot):
    while True:
        await delay()
        try:
            await handler.getUserStatus(client)
        except Exception as e:
            event.post(
                toPrint= f"Failed to save Discord Status:\nError: {e}",
                evtType= "error",
                filePath= __file__
            )
            continue
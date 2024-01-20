from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

from resource.info import PATH, ENV
from pkgs.event import event
from pkgs.wrappers.discordWrapper import Console
from app.bot.scripts import embed

import aiohttp
import aiofiles
import asyncio
import json
import nextcord
from nextcord.ext import commands
from textwrap import dedent


# Update every 2 seconds
async def delay():
    await asyncio.sleep(2)

class handler:
    
    async def getUserStatus(client: commands.Bot):
        console = Console(commands.Bot)
        guild = client.get_guild(ENV['discord']['guild']['id'])
        member = guild.get_member(ENV['discord']['USER_ID'])
        failStatus = True
        while failStatus:
            try:
                async with aiofiles.open(PATH.API.api, mode="r") as f:
                    api = json.loads(await f.read())
                failStatus = False
            except Exception as e:
                event.post(
                    toPrint=f"Failed to updated discord status:\nError: {e}",
                    evtType="error",
                    filePath=__file__
                )
                await console.error(
                    dedent(f"""
                            File: {__file__}
                            
                            Log:
                            ```json
                            {e}
                            ```
                            """),
                    title="Failed to update discord status",
                )
                await asyncio.sleep(0.5)
        
        customActivity = api["discord"]["status"]["customStatus"]
        
        if len(member.activities) != 0:
                for acti in member.activities:
                    if acti.type == nextcord.ActivityType.custom:
                        acti = acti.to_dict()
                        if (acti["type"] == 4):
                            try:
                                customActivity = f"{acti['emoji']['name']} {acti['state']}"
                            except KeyError:
                                customActivity =  f"{acti['state']}"
        toUpdate = {
                'discordStatus': member.status.name,
                'customStatus': customActivity
            }
        # print(f"""
        #       To update: {toUpdate}
        #       API: {api['discord']['status']}
        #       Compare: {api["discord"]["status"] != toUpdate}
        #       """)
        if (api["discord"]["status"] != toUpdate):
            api["discord"]["status"].update(toUpdate)
            if ENV["site"]["apiPost"] != True:
                async with aiofiles.open(PATH.API.api, mode = 'w') as f:
                    await f.write(json.dumps(api, indent=4))
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
        await handler.getUserStatus(client)
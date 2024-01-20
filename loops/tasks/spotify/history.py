from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

import asyncio
import json
from pkgs.spotify import spoti
from resource.info import PATH, ENV
from pkgs.event import event
import aiohttp
import aiofiles

# Update every 5 days
async def delay():
    days = 5
    targetSeconds = days * 24 * 60 * 60
    await asyncio.sleep(targetSeconds)

class handler:
    
    async def saveHistory():      
        spotipy = spoti.spotifyAPI()
        history = await spotipy.recentlyPlayed()

        if ENV["site"]["apiPost"] != True:
            async with aiofiles.open(PATH.API.api, mode='r') as f:
                api = json.loads(await f.read())
            
            if api["spotify"]["history"] != history:
                api["spotify"]["history"] = history
                # print(json.dumps(api, indent=4))
                
                async with aiofiles.open(PATH.API.api, mode='w') as f:
                    await f.write(json.dumps(api, indent=4))
            del api
        else:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "content": history,
                    "auth": {
                        "username": ENV["django"]["api"]["username"],
                        "passwd": ENV["django"]["api"]["passwd"]
                    }
                }
                async with session.post(
                    f"{ENV['site']['siteAddress']}/api/spotify/history",
                    json=payload
                    ) as resp:
                    print(await resp.text())
                del payload
        event.post(
            toPrint= json.dumps(history, indent=4),
            evtType= "loop",
            filePath= __file__
        )
        del history

async def run():
    while True:
        try:
            await handler.saveHistory()
            event.post(
                toPrint= "Spotify history updated",
                evtType= "loop",
                filePath= __file__
            )
        except Exception as e:
            event.post(
                toPrint= f"Spotify history failed to save:\nError: {e}",
                evtType= "error",
                filePath= __file__
            )
        await delay()
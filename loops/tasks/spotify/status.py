from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

import asyncio
import json
from pkgs.spotify import spotify, spoti
from resource.info import PATH, ENV
from pkgs.event import event
import aiohttp
import aiofiles

# Update every 1 seconds
async def delay():
    targetSeconds = 1
    await asyncio.sleep(targetSeconds)

class handler:
    
    def __init__(self):
        self.saveStatus()
    
    async def saveStatus():
        spotipy = spoti.spotifyAPI()
        curPlaying = await spotipy.currentlyPlaying()
        
        if ENV["site"]["apiPost"] != True:
            async with aiofiles.open(PATH.API.api, mode='r') as f:
                api = json.loads(await f.read())
            
            if (api["spotify"]["status"] != curPlaying):
                api["spotify"]["status"] = curPlaying
                
                async with aiofiles.open(PATH.API.api, mode='w') as f:
                    await f.write(json.dumps(api, indent=4))
                event.post(
                    toPrint= "Spotify status updated",
                    evtType= "loop",
                    filePath= __file__
                )
            del api
        else:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "content": curPlaying,
                    "auth": {
                        "username": ENV["django"]["api"]["username"],
                        "passwd": ENV["django"]["api"]["passwd"]
                    }
                }
                async with session.post(
                    f"{ENV['site']['siteAddress']}/api/spotify/status",
                    json=payload
                    ) as resp:
                    data = await resp.json()
                    if data["status"] == 200:
                        event.post(
                            toPrint= "Spotify status updated",
                            evtType= "loop",
                            filePath= __file__
                        )
                del payload
        
        del curPlaying

async def run():
    while True:
        try:
            await handler.saveStatus()
        except Exception as e:
            event.post(
                toPrint= f"Failed to save Spotify Status:\nError: {e}",
                evtType= "error",
                filePath= __file__
            )
        await delay()
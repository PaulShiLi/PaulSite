from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent.parent))

import asyncio
from pkgs.spotify.spotify import spotifyDb
from pkgs.common import event

spotify = spotifyDb()

# Update every 1 day
async def delay():
    days = 1
    targetSeconds = days * 24 * 60 * 60
    await asyncio.sleep(targetSeconds)

class handler:
    
    async def saveHistory():      
        try:
            spotify.updateDb("short_term")
        except Exception:
            spotify.reloadToken()
            event.post(
                toPrint= "Reloaded Spotify token",
                evtType= "warn",
                filePath= __file__
            )
            spotify.updateDb("short_term")
        event.post(
            toPrint= spotify.recentlyPlayed("short_term"),
            evtType= "loop",
            filePath= __file__
        )

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
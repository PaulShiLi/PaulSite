from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent))

import asyncio
from pkgs.spotify.spotify import spotifyAPI
from pkgs.common import event

spotify = spotifyAPI()

# Update every 1 seconds
async def delay():
    targetSeconds = spotify.remainingTime()
    await asyncio.sleep(targetSeconds) - 60

class handler:    
    async def refresh():
        spotify.reloadToken()
        event.post(
            toPrint= f"Spotify token refreshed. Going to refresh again in {spotify.remainingTime() - 60} seconds...",
            evtType= "loop",
            filePath= __file__
        )

async def run():
    while True:
        try:
            await handler.refresh()
        except Exception as e:
            event.post(
                toPrint= f"Failed to refresh Spotify Token:\nError: {e}",
                evtType= "error",
                filePath= __file__
            )
        await delay()
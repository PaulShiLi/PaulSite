from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent))

import asyncio
from pkgs.spotify.spotify import spotifyDb
from pkgs.common import event

spotify = spotifyDb()

# Update every 1 seconds
async def delay():
    targetSeconds = 1
    await asyncio.sleep(targetSeconds)

class handler:    
    async def saveStatus():
        # Load Spotify Status
        spotifyStatus = spotify.recentlyPlayed("current")
        if len(spotifyStatus) == 0 or spotify.spClient.currentlyPlaying()["status"] != spotifyStatus[0]["status"] and spotifyStatus[0]["platform"] == "Spotify" or spotifyStatus[0]["platform"] == "":
            # Start updating Spotify Status
            spotify.updateDb("current")
            event.post(
                toPrint= "Spotify status updated",
                evtType= "loop",
                filePath= __file__
            )
        else:
            event.post(
                toPrint= "Spotify status is up to date",
                evtType= "loop",
                filePath= __file__
            )

async def run():
    while True:
        try:
            await handler.saveStatus()
        except Exception as e:
            spotify.reloadToken()
            event.post(
                toPrint= f"Failed to save Spotify Status:\nError: {e}",
                evtType= "error",
                filePath= __file__
            )
        await delay()
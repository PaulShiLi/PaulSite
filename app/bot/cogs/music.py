from pathlib import Path
import os
import sys

sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent))

import asyncio
from yt_dlp import YoutubeDL
from urllib.parse import urlparse, parse_qs
import json

class ytdl:

    curVideo: dict = {
        "title": "",
        "url": "",
        "thumbnail": "",
        "duration": 0,
        "uploader": "",
        "date": "",
        "curDuration": 0
    }
    playlistId: str = ""
    videoId: str = ""
    queue: list = []

    def search(self, query: str):
        with YoutubeDL({"format": "bestaudio", "noplaylist": "False"}) as ydl:
            if "http" in query:
                parsedURL = urlparse(query)
                parsedQuery = parse_qs(parsedURL.query)
                if parsedURL.hostname == "www.youtube.com":
                    if "list" in parsedQuery.keys():
                        self.playlistId = parsedQuery["list"]
                    else:
                        self.playlistId = ""
                    if "v" in parsedQuery.keys():
                        self.videoId = parsedQuery["v"]
                    else:
                        self.videoId = ""
            # try:
            #     requests.get(arg)
            # except:
            #     info = ydl.extract_info(f"ytsearch:{arg}", download=False)["entries"][0]
            # else:
            info = ydl.extract_info(query, download=False)
            with open("test.json", "w") as f:
                json.dump(info, f, indent=4)
        return (info, info["formats"][0]["url"])

print(ytdl.search("https://www.youtube.com/watch?v=WAoPeG1LU1g&list=PLuNEoKb7IAjNnrpRiQoxp6oPECyx6YnZY&index=1"))
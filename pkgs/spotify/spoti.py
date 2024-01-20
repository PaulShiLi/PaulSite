from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent))
from resource.info import ENV, PATH
from pkgs.event import event

import base64
import asyncio
import aiohttp
import aiofiles
import json
from datetime import datetime

CLIENT_ID = ENV['spotify']['CLIENT_ID']
CLIENT_SECRET = ENV['spotify']['CLIENT_SECRET']
REDIRECT_URI = ENV['spotify']['REDIRECT_URI']
SCOPES = ["user-follow-read", 'user-read-playback-state', 'user-read-currently-playing', 'user-read-private',
            'user-read-email', 'user-follow-read',
            'user-library-read', 'user-read-playback-position',
            'user-top-read', 'user-read-recently-played', 'playlist-read-collaborative',
            'playlist-read-private']
API_URL = 'https://api.spotify.com/v1'
BASE_URL = "https://accounts.spotify.com"


class spotify:

    tokenData = {
        "token_Data": {},
        "expires": 0,
        "created": 0,
        "refresh_token": ""
        }
    refreshToken = ""
    code = ENV["spotify"]["CODE"]
    expires = 0

    def __init__(self):
        with open(PATH.SPOTIFY_AUTH, "r") as f:
            self.tokenData = json.load(f)
        
        self.refreshToken = self.tokenData["refresh_token"]
        
        self.expires = self.tokenData["expires"]
        
        if self.code == "":
            spotify.getCode()

    @staticmethod
    def getCode():
        fetchUrl = f"""
              {BASE_URL}/authorize
              ?client_id={CLIENT_ID}
              &response_type=code
              &redirect_uri={REDIRECT_URI}
              &scope={"%20".join(SCOPES)}
              """.replace(" ", '').replace("\n", "")
        raise ValueError(f"Please open and copy the code parameter during redirect!\n{fetchUrl}")

    async def getAccessToken(self):
        """
        Returns the following below if true
        {
            "access_token": "BQB8dXOob0PywaXcL6-iifC4g1szOCdRIM05AkORuK4I1QVdJyZ1lk8ZGempQ5je_FGOO_RuyoY7yQHJqcURLw6h81UbqFs8wXNKWABf2j6JZObXTrME0XoeXePfyEN2EmulTRD3BdxgzLtc2aFLL3MH4YqxQHOMWfmWIWipr4_bxpRvpKLDBgBO5EtP9GDRCPB_fhPjJcJryTyUcjpWoRSBCDFfyroE0YkggOLjwFpHth-OwrSgEqWUbUoZZOzY3iSV1q77acaH3kRQwcwzx9FmP1vEDX7Tpj39Z_nm8zKKxsGdrtRDcOYy7_Mt66uQeuABpHcy2m5p327VgQ",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "AQB7J_oM1fJOcEhLWvK30kBbBVUIlRGxXpfJVIxNMI6aCdD8L_hz0W8wjidl1ralJV_XfCCXLMCrzxhIXaDsqwvBXn8UNa1ZXC8grv3C7Q8qalS8NpFlWl9DeZuanpBK0m0",
            "scope": "playlist-read-private playlist-read-collaborative ugc-image-upload user-follow-read playlist-modify-private user-read-email user-read-private streaming app-remote-control user-modify-playback-state user-follow-modify user-library-read user-library-modify playlist-modify-public user-read-playback-state user-read-currently-playing user-read-recently-played user-read-playback-position user-top-read"
        }

        """
        CODE = ENV["spotify"]["CODE"]
        fetchUrl = f"""
              {BASE_URL}/api/token
              """.replace(" ", '').replace("\n", "")
        header = {
            "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {
            "grant_type": "authorization_code",
            "code": CODE,
            "redirect_uri": REDIRECT_URI
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=fetchUrl,
                headers=header,
                data=payload
            ) as resp:
                if resp.status == 400:
                    # Auth Code Expired
                    if self.refreshToken != "":
                        payload = {
                            "grant_type": "refresh_token",
                            "refresh_token": self.refreshToken
                        }
                    async with session.post(
                        url=fetchUrl,
                        headers=header,
                        data=payload
                    ) as resp:
                        if resp.status == 200:
                            await self.updateJson(tokenData=await resp.json())
                            return await resp.json()
                        else:
                            print(await resp.json())
                            spotify.getCode()
                elif resp.status == 200:
                    await spotify.updateJson(tokenData=await resp.json())
                    return await resp.json()
                elif resp.status == 429:
                    event.post(
                        "Currently rate limited!",
                        evtType= "error",
                        filePath= __file__
                    )

    async def updateJson(self, tokenData: dict):
        now = datetime.now()
        async with aiofiles.open(PATH.SPOTIFY_AUTH, mode="r") as f:
            spotify_auth = json.loads(await f.read())
        
        # Set token expire to 5 minutes before just in case of time delay
        spotify_auth["expires"] = now.timestamp() + (tokenData["expires_in"]) - (5 * 60)
        spotify_auth["created"] = now.timestamp()
        spotify_auth["token_Data"] = tokenData
        if "refresh_token" in tokenData:
            spotify_auth["refresh_token"] = tokenData["refresh_token"]
            self.refreshToken = spotify_auth["refresh_token"]
        self.expires = spotify_auth["expires"]
        self.tokenData = spotify_auth
        async with aiofiles.open(PATH.SPOTIFY_AUTH, mode="w") as f:
            await f.write(json.dumps(spotify_auth, indent=4))
        event.post(
            toPrint="Updated spotify_auth.json",
            evtType="loop",
            filePath=__file__
        )

    async def readJson(self):
        with open(PATH.SPOTIFY_AUTH, "r") as f:
            if self.tokenData != json.load(f):
                self.tokenData = json.load(f)
                self.refreshToken = self.tokenData["refresh_token"]
                now = datetime.now()
                self.expires = self.tokenData["expires"]
                if self.expires < now.timestamp():
                    self.getAccessToken()
            else:
                self.getAccessToken()

    async def getHistory(self, time_range: str, limit: int = 50):
        """
        limit <int>:
        Maxmimum numer of items to return
        
        
        timeRange <str>:
        "short_term"    (history from ~ 4 weeks)
        "medium_term"   (history from ~ 6 months)
        "long_term"     (history from several years)
        """
        now = datetime.now()
        if self.expires < now.timestamp():
            await self.getAccessToken()
        fetchUrl = f"""
              {API_URL}/me/top/tracks
              ?limit={limit}
              &time_range={time_range}
              """.replace(" ", '').replace("\n", "")
        header = {
            "Authorization": f"{self.tokenData['token_Data']['token_type']} {self.tokenData['token_Data']['access_token']}",
            "Content-Type": "Content-Type: application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=fetchUrl,
                headers=header,
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 429:
                    event.post(
                        "Currently rate limited!",
                        evtType= "error",
                        filePath= __file__
                    )
                elif resp.status == 400:
                    self.readJson()
                    async with session.get(
                        url=fetchUrl,
                        headers=header,
                    ) as resp:
                        if resp.status == 200:
                            return await resp.json()
                        elif resp.status == 429:
                            event.post(
                                "Currently rate limited!",
                                evtType= "error",
                                filePath= __file__
                            )
                        elif resp.status == 400:
                            event.post(
                                f"Unable to fetch spotify history:\nError: {await resp.text()}",
                                evtType="error",
                                filePath=__file__
                            )

    async def recentlyPlayed(self, limit:int = 50):
        now = datetime.now()
        if self.expires < now.timestamp():
            await self.getAccessToken()
        fetchUrl = f"""
              {API_URL}/me/player/recently-played
              ?limit={limit}
              """.replace(" ", '').replace("\n", "")
        header = {
            "Authorization": f"{self.tokenData['token_Data']['token_type']} {self.tokenData['token_Data']['access_token']}",
            "Content-Type": "Content-Type: application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=fetchUrl,
                headers=header,
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 429:
                    event.post(
                        "Currently rate limited!",
                        evtType= "error",
                        filePath= __file__
                    )
                elif resp.status == 400:
                    self.readJson()
                    async with session.get(
                        url=fetchUrl,
                        headers=header,
                    ) as resp:
                        if resp.status == 200:
                            return await resp.json()
                        elif resp.status == 429:
                            event.post(
                                "Currently rate limited!",
                                evtType= "error",
                                filePath= __file__
                            )
                        elif resp.status == 400:
                            event.post(
                                f"Unable to fetch spotify history:\nError: {await resp.text()}",
                                evtType="error",
                                filePath=__file__
                            )

    async def currentlyPlaying(self):
        now = datetime.now()
        if self.expires < now.timestamp():
            await self.getAccessToken()
        fetchUrl = f"""
              {API_URL}/me/player/currently-playing
              """.replace(" ", '').replace("\n", "")
        header = {
            "Authorization": f"{self.tokenData['token_Data']['token_type']} {self.tokenData['token_Data']['access_token']}",
            "Content-Type": "Content-Type: application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=fetchUrl,
                headers=header,
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 429:
                    event.post(
                        "Currently rate limited!",
                        evtType= "error",
                        filePath= __file__
                    )
                elif resp.status == 400:
                    self.readJson()
                    async with session.get(
                        url=fetchUrl,
                        headers=header,
                    ) as resp:
                        if resp.status == 200:
                            return await resp.json()
                        elif resp.status == 429:
                            event.post(
                                "Currently rate limited!",
                                evtType= "error",
                                filePath= __file__
                            )
                        elif resp.status == 400:
                            event.post(
                                f"Unable to fetch spotify history:\nError: {await resp.text()}",
                                evtType="error",
                                filePath=__file__
                            )

class spotifyAPI():
    def __init__(self):
        self.spotify = spotify()
        pass
    
    def retrieveSongs(self, songList: dict, listType: str = "None"):
        totalSongs = []
        # print(f"\n{listType}\n")
        if listType == "recents":
            while songList:
                for i, track in enumerate(songList['items']):
                    songName = track["track"]["name"]
                    songArtist = track["track"]["artists"][0]["name"]
                    songLink = track["track"]["external_urls"]["spotify"]
                    songPic = track["track"]["album"]["images"][0]["url"]
                    releaseDate = track["track"]["album"]["release_date"]
                    # print(f"Songs: {songName}")
                    # print(f"Artists: {songArtist}")
                    # print(f"Link: {songLink}")
                    # print(f"Pic: {songPic}")
                    # print(f"Release Date: {releaseDate}")
                    # print("--------------------------------------------------")
                    updatedSong = {
                        "name": songName,
                        "artist": songArtist,
                        "link": songLink,
                        "pic": songPic,
                        "releaseDate": releaseDate
                    }
                    totalSongs.append(updatedSong)
                if songList['next']:
                    songList = self.user.next(songList)
                else:
                    songList = None
        else:
            while songList:
                for i, track in enumerate(songList['items']):
                    songName = track["name"]
                    songArtist = track["artists"][0]["name"]
                    songLink = track["external_urls"]["spotify"]
                    songPic = track["album"]["images"][0]["url"]
                    releaseDate = track["album"]["release_date"]
                    # print(f"Songs: {songName}")
                    # print(f"Artists: {songArtist}")
                    # print(f"Link: {songLink}")
                    # print(f"Pic: {songPic}")
                    # print(f"Release Date: {releaseDate}")
                    # print("--------------------------------------------------")
                    updatedSong = {
                        "name": songName,
                        "artist": songArtist,
                        "link": songLink,
                        "pic": songPic,
                        "releaseDate": releaseDate
                    }
                    totalSongs.append(updatedSong)
                if songList['next']:
                    songList = self.user.next(songList)
                else:
                    songList = None
        return totalSongs

    async def recentlyPlayed(self):
        # Get recently played songs
        recents = await self.spotify.recentlyPlayed()
        # Get songs played short term
        shortTerm = await self.spotify.getHistory(
            time_range='short_term', limit=50)
        # Get songs played medium term
        mediumTerm = await self.spotify.getHistory(
            time_range='medium_term', limit=50)
        # Get songs played long term
        longTerm = await self.spotify.getHistory(
            time_range='long_term', limit=50)
        # print(f"Recents: {recents}")
        # print(f"Short Term: {shortTerm}")

        totalSongs = {
            "recents": {},
            "mediumTerm": {},
            "longTerm": {}
        }

        # Get the current data
        if len(shortTerm['items']) == 0:
            totalSongs['recents'] = self.retrieveSongs(
                recents, "recents")[::-1]
            # print(self.retrieveSongs(recents, "recents"))
        else:
            # Get the songs played short term
            totalSongs['recents'] = self.retrieveSongs(
                shortTerm, "shortTerm")[::-1]

        # Get the songs played medium term
        totalSongs['mediumTerm'] = self.retrieveSongs(
            mediumTerm, "mediumTerm")[::-1]
        # Get the songs played long term
        totalSongs['longTerm'] = self.retrieveSongs(longTerm, "longTerm")[::-1]
        totalSongs.update({
            'status': "totalSongs"
        })
        return totalSongs

    async def currentlyPlaying(self):
        # Get the current song playing
        currentSong = await self.spotify.currentlyPlaying()
        # print(currentSong)
        try:
            if currentSong is None:
                return {
                    'status': 'noCurrentSong'
                }
            else:
                songName = currentSong["item"]["name"]
                songArtist = currentSong["item"]["artists"][0]["name"]
                artistLink = currentSong["item"]["artists"][0]["external_urls"]["spotify"]
                songLink = currentSong["item"]["external_urls"]["spotify"]
                songPic = currentSong["item"]["album"]["images"][0]["url"]
                releaseDate = currentSong["item"]["album"]["release_date"]
                currentDuration = currentSong["progress_ms"]
                totalDuration = currentSong["item"]["duration_ms"]
                # print(f"Songs: {songName}")
                # print(f"Artists: {songArtist}")
                # print(f"Link: {songLink}")
                # print(f"Pic: {songPic}")
                # print(f"Release Date: {releaseDate}")
                # print("--------------------------------------------------")
                updatedSong = {
                    "name": songName,
                    "artist": songArtist,
                    "artistLink": artistLink,
                    "link": songLink,
                    "pic": songPic,
                    "releaseDate": releaseDate,
                    "currentDuration": currentDuration,
                    "totalDuration": totalDuration,
                    'status': "currentSong"
                }
                return updatedSong
        except:
            return {
                'status': 'noCurrentSong'
            }

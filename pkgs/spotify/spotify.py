import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import spotipy
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from typing import Literal
import orjson
import time

from pkgs.mongo.db import Mongo, mongoClient
from pkgs import ENV, ASSETS_DIR

class spotifyAPI:
    # Load secret from environment variable
    scopes = ["user-follow-read", 'ugc-image-upload', 'user-read-playback-state',
              'user-modify-playback-state', 'user-read-currently-playing', 'user-read-private',
              'user-read-email', 'user-follow-modify', 'user-follow-read', 'user-library-modify',
              'user-library-read', 'streaming', 'app-remote-control', 'user-read-playback-position',
              'user-top-read', 'user-read-recently-played', 'playlist-modify-private', 'playlist-read-collaborative',
              'playlist-read-private', 'playlist-modify-public']
    baseUrl = 'https://api.spotify.com/v1/'
    cachePath = ASSETS_DIR / "storage" / "spotify" / ".token"

    def __init__(self):
        # Header to start accessing Spotify Data
        self.user = spotipy.Spotify(
            auth_manager = SpotifyOAuth(
                client_id=ENV.content['spotify']['CLIENT_ID'],
                client_secret=ENV.content['spotify']['CLIENT_SECRET'],
                redirect_uri=ENV.content['spotify']['REDIRECT_URI'],
                scope=self.scopes,
                username=ENV.content['spotify']['USER_ID'],
                cache_handler=CacheFileHandler(
                    cache_path=self.cachePath
                ),
            )
        )
    
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
                        "_id": len(songList['items'])-1-i,
                        "name": songName,
                        "artist": songArtist,
                        "link": songLink,
                        "pic": songPic,
                        "releaseDate": releaseDate
                    }
                    totalSongs.append(updatedSong)
                # if songList['next']:
                #     songList = self.user.next(songList)
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
                        "_id": len(songList['items'])-1-i,
                        "name": songName,
                        "artist": songArtist,
                        "link": songLink,
                        "pic": songPic,
                        "releaseDate": releaseDate
                    }
                    totalSongs.append(updatedSong)
                # if songList['next']:
                #     songList = self.user.next(songList)
                else:
                    songList = None
        return totalSongs

    def recentlyPlayed(self, timeRange: Literal['short_term', 'medium_term', 'long_term'] = 'short_term', limit: int = 50):
        term = self.user.current_user_top_tracks(time_range=timeRange, limit=limit)

        songList = {}

        # Get the current data
        if len(term['items']) == 0 and timeRange == 'short_term':
            songList = self.retrieveSongs(
                self.user.current_user_recently_played(), "recents")[::-1]
            # print(self.retrieveSongs(recents, "recents"))
        else:
            # Get the songs played short term
            songList = self.retrieveSongs(term, "shortTerm")[::-1]

        return songList

    def currentlyPlaying(self):
        # Get the current song playing
        currentSong = self.user.current_user_playing_track()
        # print(currentSong)
        try:
            if currentSong is None:
                updatedSong = {
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
        except:
            updatedSong = {
                'status': 'noCurrentSong'
            }
        updatedSong.update({
            "_id": 0,
            "platform": "Spotify" if updatedSong['status'] == 'currentSong' else ""
        })
        return updatedSong

    def reloadToken(self):
        # Get the current song playing
        token = util.prompt_for_user_token(
            ENV.content['spotify']['USER_ID'],
            scope=self.scopes,
            client_id=ENV.content['spotify']['CLIENT_ID'],
            client_secret=ENV.content['spotify']['CLIENT_SECRET'],
            redirect_uri=ENV.content['spotify']['REDIRECT_URI'],
            cache_path=self.cachePath
        )
        return token

    def remainingTime(self):
        with open(self.cachePath, 'r') as f:
            token = orjson.loads(f.read())
        remainingTime = token["expires_at"] - time.time()
        return remainingTime if remainingTime > 0 else 0

class spotifyDb():
    spClient = spotifyAPI()
    
    def __init__(self):       
        try:
            self.spClient.currentlyPlaying()
        except:
            self.spClient.reloadToken()

    def updateDb(self, timeRange: Literal['short_term', 'medium_term', 'long_term', 'current'] = 'short_term', limit: int = 50):
        if timeRange not in ['short_term', 'medium_term', 'long_term', 'current']:
            raise ValueError("Invalid time range")
        
        
        if timeRange in mongoClient["spotify"].list_collection_names():
            # Remove all documents in the collection
            Mongo.delete("spotify", timeRange)
        
        if timeRange == 'current':
            songList = self.spClient.currentlyPlaying()
        else:
            songList = self.spClient.recentlyPlayed(timeRange, limit)
        
        Mongo.insert("spotify", timeRange, songList)
    
    def recentlyPlayed(self, timeRange: Literal['short_term', 'medium_term', 'long_term', 'current'] = 'short_term') -> list:
        if timeRange not in ['short_term', 'medium_term', 'long_term', 'current']:
            raise ValueError("Invalid time range")
        
        return list(Mongo.find("spotify", timeRange))

    def reloadToken(self):
        return self.spClient.reloadToken()

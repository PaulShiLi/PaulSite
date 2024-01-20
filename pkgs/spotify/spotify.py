import spotipy
from spotipy.oauth2 import SpotifyOAuth

from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent))
from resource.info import ENV

class spotifyAPI:
    # Load secret from environment variable
    clientID = ENV['spotify']['CLIENT_ID']
    clientSecret = ENV['spotify']['CLIENT_SECRET']
    redirectURI = ENV['spotify']['REDIRECT_URI']
    scopes = ["user-follow-read", 'ugc-image-upload', 'user-read-playback-state',
              'user-modify-playback-state', 'user-read-currently-playing', 'user-read-private',
              'user-read-email', 'user-follow-modify', 'user-follow-read', 'user-library-modify',
              'user-library-read', 'streaming', 'app-remote-control', 'user-read-playback-position',
              'user-top-read', 'user-read-recently-played', 'playlist-modify-private', 'playlist-read-collaborative',
              'playlist-read-private', 'playlist-modify-public']
    baseUrl = 'https://api.spotify.com/v1/'

    def __init__(self):
        # Header to start accessing Spotify Data
        self.user = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.clientID,
            client_secret=self.clientSecret,
            redirect_uri=self.redirectURI,
            scope=self.scopes
        ))

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

    def recentlyPlayed(self):
        # Get recently played songs
        recents = self.user.current_user_recently_played()
        # Get songs played short term
        shortTerm = self.user.current_user_top_tracks(
            time_range='short_term', limit=50)
        # Get songs played medium term
        mediumTerm = self.user.current_user_top_tracks(
            time_range='medium_term', limit=50)
        # Get songs played long term
        longTerm = self.user.current_user_top_tracks(
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

    def currentlyPlaying(self):
        # Get the current song playing
        currentSong = self.user.current_user_playing_track()
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

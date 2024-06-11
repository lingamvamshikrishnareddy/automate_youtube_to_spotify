import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import sys
import codecs

# Set stdout encoding to UTF-8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# YouTube API setup
YOUTUBE_API_KEY = 'AIzaSyAIvlT3phv-aiszYkS_gsCXKJniemPUWfU'  # Replace with your new API key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_PLAYLIST_ID = 'PLa-l7fs8jYIP95BdEYbb6_HN9Uw6FmW7w'  # Replace with your YouTube playlist ID

# Spotify API setup
SPOTIPY_CLIENT_ID = '0dac2d20ea674269832f6e1f93eb99e6'  # Replace with your Spotify Client ID
SPOTIPY_CLIENT_SECRET = '9b0764a5a97e4559a7b4aeb7b8db1a48'  # Replace with your Spotify Client Secret
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SPOTIFY_PLAYLIST_ID = '3epBNqeSt0vNpGG2VssQyB'  # Replace with your Spotify playlist ID

def get_youtube_songs(api_key, playlist_id):
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    songs = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=playlist_id,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            title = item['snippet']['title']
            # Sanitize the title
            title = title.encode('utf-8', errors='ignore').decode('utf-8')
            songs.append(title)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return songs

def create_spotify_client():
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIPY_REDIRECT_URI,
                                                   scope=scope))
    return sp

def search_spotify(sp, song_name):
    results = sp.search(q=song_name, limit=1, type='track')
    tracks = results['tracks']['items']
    if tracks:
        return tracks[0]['id']
    else:
        return None

def add_song_to_spotify(sp, track_id, playlist_id):
    sp.playlist_add_items(playlist_id, [track_id])

def main():
    youtube_songs = get_youtube_songs(YOUTUBE_API_KEY, YOUTUBE_PLAYLIST_ID)
    sp = create_spotify_client()

    for song in youtube_songs:
        track_id = search_spotify(sp, song)
        if track_id:
            add_song_to_spotify(sp, track_id, SPOTIFY_PLAYLIST_ID)
            print(f'Added {song} to Spotify playlist'.encode('utf-8', errors='replace').decode('utf-8'))
        else:
            print(f'Could not find {song} on Spotify'.encode('utf-8', errors='replace').decode('utf-8'))

if __name__ == "__main__":
    main()

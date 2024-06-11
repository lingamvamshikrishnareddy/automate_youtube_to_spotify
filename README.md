# automate_youtube_to_spotify
YouTube to Spotify Playlist Transfer Script
This script automates the process of transferring songs from a YouTube playlist to a Spotify playlist using YouTube Data API and Spotify Web API.

Prerequisites
Python: Make sure you have Python installed. You can download it from python.org.
Required Libraries: Install the necessary Python libraries:
sh
Copy code
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client spotipy requests
YouTube API Setup
Create a Google Cloud Project:

Go to the Google Cloud Console.
Sign in with your Google account.
Click on the project drop-down and select "New Project".
Enter a project name and click "Create".
Enable YouTube Data API:

In the Google Cloud Console, navigate to "APIs & Services" > "Library".
Search for "YouTube Data API v3" and click on it.
Click "Enable" to enable the API for your project.
Create API Key:

Go to "APIs & Services" > "Credentials".
Click on "Create Credentials" and select "API key".
Copy the API key displayed. This will be your YOUTUBE_API_KEY.
Find YouTube Playlist ID:

Open your playlist on YouTube.
The playlist ID is the part of the URL after list=. For example, in https://www.youtube.com/playlist?list=PL12345, PL12345 is the playlist ID.
Spotify API Setup
Create a Spotify Developer Account:

Go to the Spotify Developer Dashboard.
Log in or sign up for a Spotify Developer account.
Create a New Application:

Click on "Create an App".
Enter an app name and description, and click "Create".
Note the Client ID and Client Secret.
Set Redirect URI:

Click on "Edit Settings" in your application's dashboard.
Add http://localhost:8888/callback to the Redirect URIs and save.
Find Spotify Playlist ID:

Open your playlist on Spotify.
The playlist ID is the part of the URL after https://open.spotify.com/playlist/. For example, in https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M, 37i9dQZF1DXcBWIGoYBM5M is the playlist ID.
Script Setup
Create the Script:
Create a Python file (e.g., songs_automate.py) and copy the following code into it:
python



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
YOUTUBE_API_KEY = 'YOUR_NEW_YOUTUBE_API_KEY'  # Replace with your new API key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_PLAYLIST_ID = 'YOUR_YOUTUBE_PLAYLIST_ID'  # Replace with your YouTube playlist ID

# Spotify API setup
SPOTIPY_CLIENT_ID = 'YOUR_SPOTIPY_CLIENT_ID'  # Replace with your Spotify Client ID
SPOTIPY_CLIENT_SECRET = 'YOUR_SPOTIPY_CLIENT_SECRET'  # Replace with your Spotify Client Secret
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SPOTIFY_PLAYLIST_ID = 'YOUR_SPOTIFY_PLAYLIST_ID'  # Replace with your Spotify playlist ID

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




    
Replace Placeholders:
Replace YOUR_NEW_YOUTUBE_API_KEY with your YouTube API key.
Replace YOUR_YOUTUBE_PLAYLIST_ID with your YouTube playlist ID.
Replace YOUR_SPOTIPY_CLIENT_ID with your Spotify Client ID.
Replace YOUR_SPOTIPY_CLIENT_SECRET with your Spotify Client Secret.
Replace YOUR_SPOTIFY_PLAYLIST_ID with your Spotify playlist ID.
Running the Script
Run the Script:
sh
Copy code
python songs_automate.py
This script will retrieve all songs from your specified YouTube playlist, search for them on Spotify, and add them to your specified Spotify playlist. The script handles pagination to ensure all songs are retrieved and added.

Troubleshooting
Unicode Errors: If you encounter UnicodeEncodeError, ensure that the console encoding is set to UTF-8 and that song titles are sanitized.
Missing Songs: If some songs are not found on Spotify, verify the song titles manually and consider tweaking the search logic to improve accuracy.
This documentation provides all the necessary steps and explanations to set up and run the script successfully.

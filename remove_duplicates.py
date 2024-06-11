import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your actual credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback'  # This should match the redirect URI in your Spotify Developer Dashboard

# Define the scope for the authorization
scope = 'playlist-read-private playlist-modify-public playlist-modify-private'

# Authenticate and get the token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Function to get all tracks from a playlist
def get_playlist_tracks(playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        return tracks
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return []

# Function to remove duplicate songs by name
def remove_duplicates(playlist_id):
    tracks = get_playlist_tracks(playlist_id)
    if not tracks:
        print("No tracks found or unable to retrieve tracks.")
        return
    
    seen = {}
    duplicates = []

    # Identify duplicates
    for item in tracks:
        track = item['track']
        track_id = track['id']
        track_name = track['name']
        if track_name in seen:
            duplicates.append(track_id)
        else:
            seen[track_name] = track_id
    
    # Remove duplicates in batches of 100
    BATCH_SIZE = 100
    for i in range(0, len(duplicates), BATCH_SIZE):
        batch = duplicates[i:i+BATCH_SIZE]
        sp.playlist_remove_all_occurrences_of_items(playlist_id, batch)
        print(f"Removed {len(batch)} duplicate tracks in this batch.")

    print(f"Total duplicates removed: {len(duplicates)}")

# Example usage
playlist_id = 'YOUR_PLAYLIST_ID'
remove_duplicates(playlist_id)

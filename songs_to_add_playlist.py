import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your actual credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback'  # This should match the redirect URI in your Spotify Developer Dashboard

# Define the scope for the authorization
scope = 'user-library-read playlist-modify-public playlist-modify-private'

# Authenticate and get the token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Function to get all liked tracks
def get_liked_tracks():
    results = sp.current_user_saved_tracks()
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Function to add tracks to a playlist
def add_tracks_to_playlist(playlist_id, track_ids):
    BATCH_SIZE = 100
    for i in range(0, len(track_ids), BATCH_SIZE):
        batch = track_ids[i:i+BATCH_SIZE]
        sp.playlist_add_items(playlist_id, batch)
        print(f"Added {len(batch)} tracks to the playlist.")

# Main script
liked_tracks = get_liked_tracks()
track_ids = [track['track']['id'] for track in liked_tracks]

# Specify your target playlist ID
playlist_id = 'YOUR_PLAYLIST_ID'
add_tracks_to_playlist(playlist_id, track_ids)

print(f"Total tracks added to the playlist: {len(track_ids)}")

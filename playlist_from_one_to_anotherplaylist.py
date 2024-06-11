import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='YOUR_CLIENT_ID',
                                               client_secret='YOUR_CLIENT_SECRET',
                                               redirect_uri='YOUR_REDIRECT_URI',
                                               scope='playlist-modify-public'))

# Function to add tracks to a playlist
def add_to_playlist(source_playlist_id, destination_playlist_id):
    # Get tracks from source playlist
    source_tracks = sp.playlist_tracks(source_playlist_id)['items']
    track_ids = [track['track']['id'] for track in source_tracks]

    # Add tracks to destination playlist
    sp.playlist_add_items(destination_playlist_id, track_ids)
    print(f"Added {len(track_ids)} tracks to the destination playlist.")

# Example usage
if __name__ == "__main__":
    source_playlist_id = 'SOURCE_PLAYLIST_ID'
    destination_playlist_id = 'DESTINATION_PLAYLIST_ID'
    add_to_playlist(source_playlist_id, destination_playlist_id)

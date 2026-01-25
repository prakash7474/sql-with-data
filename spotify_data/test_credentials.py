import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Test Spotify API credentials
client_id = '3ca6426adfa44b62a0b063b2f0c3ef9c'
client_secret = 'd8e6ece060f14a99a6629f4fd10f5623'

try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

    # Test with a known track
    track_id = '0zsA45R0SQPfqC5TyDOqY8'
    track = sp.track(track_id)

    print("✅ Credentials are working!")
    print(f"Track Name: {track['name']}")
    print(f"Artist: {track['artists'][0]['name']}")
    print(f"Album: {track['album']['name']}")

    # Test audio features
    audio_features = sp.audio_features([track_id])[0]
    print(f"Danceability: {audio_features['danceability']}")

except Exception as e:
    print(f"❌ Credentials test failed: {e}")

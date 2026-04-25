import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Test Spotify API credentials
client_id = '11f96fb384e44b92821fd86b7c9f2967'
client_secret = '5d0f71fd70964717ad4e99bd8aa21708'

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

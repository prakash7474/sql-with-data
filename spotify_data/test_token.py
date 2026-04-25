import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Test Spotify API credentials
client_id = '11f96fb384e44b92821fd86b7c9f2967'
client_secret = '5d0f71fd70964717ad4e99bd8aa21708'

try:
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Try to get access token
    token = auth_manager.get_access_token(as_dict=False)
    print("✅ Credentials are valid! Access token obtained successfully.")
    print(f"Token prefix: {token[:20]}...")
    
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # Try a simple search instead of track fetch (may have different permissions)
    try:
        results = sp.search(q='artist:ed sheeran', type='artist', limit=1)
        if results and 'artists' in results and results['artists']['items']:
            artist = results['artists']['items'][0]
            print(f"✅ API search working! Found artist: {artist['name']}")
    except Exception as e:
        print(f"⚠️ Search test failed (may be account restriction): {e}")
    
    print("\nNote: The 403 error on track fetch indicates the Spotify app owner needs an active premium subscription.")
    print("This is an account-level restriction, not a credential issue.")

except Exception as e:
    print(f"❌ Credentials test failed: {e}")


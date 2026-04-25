import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='11f96fb384e44b92821fd86b7c9f2967',  
    client_secret='5d0f71fd70964717ad4e99bd8aa21708'  
))

# MySQL Database Connection
db_config = {
    'host': 'localhost',          
    'port': 3306,
    'user': 'root',       
    'password': 'P@ssw0rd',   
    'database': 'spotify_db'     
}

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()


track_url = "https://open.spotify.com/track/6sPW145Y3LSXd4p1LjBOcS"


track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)


track = sp.track(track_id)
print(track)

track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}
print(f"\ntrack_data: {track_data['Track Name']}")
print(f"\nArtist: {track_data['Artist']}")
print(f"\nAlbum: {track_data['Album']}")  
print(f"\nPopularity: {track_data['Popularity']}")
print(f"\nDuration (minutes): {track_data['Duration (minutes)']:.2f} minutes")
print("\n data frame :\n")

df = pd.DataFrame([track_data])
##print(df)

df.to_csv('track_data.csv', mode='a', index=False, header=not pd.io.common.file_exists('track_data.csv'))
features=['popularity','duration_ms']
values = [track_data['Popularity'], track_data['Duration (minutes)']]
plt.figure(figsize=(10, 5))
plt.bar(features, values, color=['blue', 'orange'])
plt.title(f"Track Features: {track_data['Track Name']}")
plt.ylabel('Value') 
plt.show()
# Insert data into MySQL
insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)']
))
connection.commit()

print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into the database.")
cursor.close()
connection.close()



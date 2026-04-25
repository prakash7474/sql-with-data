from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector
import re
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Spotify API setup
# IMPORTANT: Replace these with your actual Spotify API credentials
# Get them from: https://developer.spotify.com/dashboard
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='11f96fb384e44b92821fd86b7c9f2967',  # Replace with your Client ID
    client_secret='5d0f71fd70964717ad4e99bd8aa21708'  # Replace with your Client Secret
))

# MySQL Database Connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='P@ssw0rd',
        database='spotify_db'
    )

def extract_spotify_id(url, type='track'):
    """Extract Spotify ID from URL"""
    pattern = rf'{type}/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_or_create_artist(artist_name, cursor):
    """Get artist ID or create new artist"""
    cursor.execute("SELECT artist_id FROM artists WHERE name = %s", (artist_name,))
    result = cursor.fetchone()
    if result:
        return result[0]

    cursor.execute("INSERT INTO artists (name) VALUES (%s)", (artist_name,))
    return cursor.lastrowid

def get_or_create_album(album_name, artist_id, cursor):
    """Get album ID or create new album"""
    cursor.execute("SELECT album_id FROM albums WHERE name = %s AND artist_id = %s",
                   (album_name, artist_id))
    result = cursor.fetchone()
    if result:
        return result[0]

    cursor.execute("INSERT INTO albums (name, artist_id) VALUES (%s, %s)",
                   (album_name, artist_id))
    return cursor.lastrowid

def insert_track(track_data, audio_features=None):
    """Insert track and related data into database"""
    connection = None
    cursor = None
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Get or create artist
        artist_id = get_or_create_artist(track_data['artists'][0]['name'], cursor)

        # Get or create album
        album_id = get_or_create_album(track_data['album']['name'], artist_id, cursor)

        # Insert track
        cursor.execute("""
            INSERT INTO tracks (name, artist_id, album_id, popularity, duration_ms, spotify_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE popularity = VALUES(popularity)
        """, (
            track_data['name'],
            artist_id,
            album_id,
            track_data['popularity'],
            track_data['duration_ms'],
            track_data['id']
        ))

        track_id = cursor.lastrowid or cursor.execute("SELECT track_id FROM tracks WHERE spotify_id = %s", (track_data['id'],)) or cursor.fetchone()[0]

        # Insert audio features if provided
        if audio_features:
            cursor.execute("""
                INSERT INTO audio_features
                (track_id, danceability, energy, key, loudness, mode, speechiness,
                 acousticness, instrumentalness, liveness, valence, tempo, duration_ms,
                 time_signature)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE track_id = track_id
            """, (
                track_id,
                audio_features.get('danceability'),
                audio_features.get('energy'),
                audio_features.get('key'),
                audio_features.get('loudness'),
                audio_features.get('mode'),
                audio_features.get('speechiness'),
                audio_features.get('acousticness'),
                audio_features.get('instrumentalness'),
                audio_features.get('liveness'),
                audio_features.get('valence'),
                audio_features.get('tempo'),
                audio_features.get('duration_ms'),
                audio_features.get('time_signature')
            ))

        connection.commit()
        return track_id

    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/analyze-track', methods=['POST'])
def analyze_track():
    try:
        data = request.get_json()
        url = data.get('url')
        source = data.get('source', 'api')  # 'api' for Spotify API, 'static' for CSV data

        if source == 'static':
            # Analyze static CSV data
            return analyze_static_track_data(data)
        else:
            # Analyze Spotify API data
            if not url:
                return jsonify({"error": "URL is required"}), 400

            track_id = extract_spotify_id(url, 'track')
            if not track_id:
                return jsonify({"error": "Invalid Spotify track URL"}), 400

            # Fetch track data
            track = sp.track(track_id)

            # Fetch audio features
            audio_features = sp.audio_features([track_id])[0]

            # Insert into database
            insert_track(track, audio_features)

            # Prepare response
            response = {
                "id": track['id'],
                "name": track['name'],
                "artists": track['artists'],
                "album": track['album'],
                "popularity": track['popularity'],
                "duration_ms": track['duration_ms'],
                "external_urls": track['external_urls'],
                "audio_features": audio_features
            }

            return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def analyze_static_track_data(data):
    """Analyze static track data from CSV files"""
    try:
        import pandas as pd
        import os

        # Read static CSV files
        track_data_path = os.path.join(os.getcwd(), 'track_data.csv')
        spotify_track_data_path = os.path.join(os.getcwd(), 'spotify_track_data.csv')

        tracks_data = []

        # Read track_data.csv
        if os.path.exists(track_data_path):
            df1 = pd.read_csv(track_data_path)
            for _, row in df1.iterrows():
                tracks_data.append({
                    "name": row['Track Name'],
                    "artists": [{"name": row['Artist']}],
                    "album": {"name": row['Album']},
                    "popularity": int(row['Popularity']),
                    "duration_ms": int(float(row['Duration (minutes)']) * 60000),  # Convert to ms
                    "id": f"static_{len(tracks_data)}",
                    "audio_features": None  # No audio features in static data
                })

        # Read spotify_track_data.csv
        if os.path.exists(spotify_track_data_path):
            df2 = pd.read_csv(spotify_track_data_path)
            for _, row in df2.iterrows():
                tracks_data.append({
                    "name": row['Track Name'],
                    "artists": [{"name": row['Artist']}],
                    "album": {"name": row['Album']},
                    "popularity": int(row['Popularity']),
                    "duration_ms": int(float(row['Duration (minutes)']) * 60000),  # Convert to ms
                    "id": f"static_{len(tracks_data)}",
                    "audio_features": None  # No audio features in static data
                })

        # Insert static data into database
        connection = create_connection()
        cursor = connection.cursor()

        for track_data in tracks_data:
            # Get or create artist
            artist_id = get_or_create_artist(track_data['artists'][0]['name'], cursor)

            # Get or create album
            album_id = get_or_create_album(track_data['album']['name'], artist_id, cursor)

            # Insert track
            cursor.execute("""
                INSERT INTO tracks (name, artist_id, album_id, popularity, duration_ms, spotify_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE popularity = VALUES(popularity)
            """, (
                track_data['name'],
                artist_id,
                album_id,
                track_data['popularity'],
                track_data['duration_ms'],
                track_data['id']
            ))

        connection.commit()

        # Return analysis results
        response = {
            "type": "static_analysis",
            "total_tracks": len(tracks_data),
            "tracks": tracks_data,
            "message": f"Successfully analyzed {len(tracks_data)} tracks from static data"
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Error analyzing static data: {str(e)}"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/api/analyze-playlist', methods=['POST'])
def analyze_playlist():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "URL is required"}), 400

        playlist_id = extract_spotify_id(url, 'playlist')
        if not playlist_id:
            return jsonify({"error": "Invalid Spotify playlist URL"}), 400

        # Fetch playlist data
        playlist = sp.playlist(playlist_id)

        # Get all tracks from playlist
        tracks = []
        results = sp.playlist_tracks(playlist_id)
        tracks.extend(results['items'])

        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        # Process tracks
        processed_tracks = []
        track_ids = [track['track']['id'] for track in tracks if track['track']]

        # Fetch audio features in batches
        audio_features_list = []
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            audio_features_list.extend(sp.audio_features(batch))

        for i, track_item in enumerate(tracks):
            if not track_item['track']:
                continue

            track = track_item['track']
            audio_features = audio_features_list[i] if i < len(audio_features_list) else None

            # Insert into database
            insert_track(track, audio_features)

            processed_tracks.append({
                "id": track['id'],
                "name": track['name'],
                "artists": track['artists'],
                "album": track['album'],
                "popularity": track['popularity'],
                "duration_ms": track['duration_ms'],
                "audio_features": audio_features
            })

        response = {
            "name": playlist['name'],
            "description": playlist['description'],
            "total_tracks": len(processed_tracks),
            "tracks": processed_tracks
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tracks', methods=['GET'])
def get_tracks():
    connection = None
    cursor = None
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT t.track_id as id, t.name, ar.name as artist, al.name as album,
                   t.popularity, t.duration_ms, t.spotify_id
            FROM tracks t
            JOIN artists ar ON t.artist_id = ar.artist_id
            JOIN albums al ON t.album_id = al.album_id
            ORDER BY t.track_id DESC
        """)

        tracks = cursor.fetchall()
        return jsonify({"tracks": tracks})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/stats', methods=['GET'])
def get_stats():
    connection = None
    cursor = None
    try:
        connection = create_connection()
        cursor = connection.cursor()

        stats = {}

        # Total tracks
        cursor.execute("SELECT COUNT(*) FROM tracks")
        stats['total_tracks'] = cursor.fetchone()[0]

        # Total artists
        cursor.execute("SELECT COUNT(*) FROM artists")
        stats['total_artists'] = cursor.fetchone()[0]

        # Total albums
        cursor.execute("SELECT COUNT(*) FROM albums")
        stats['total_albums'] = cursor.fetchone()[0]

        # Average popularity
        cursor.execute("SELECT AVG(popularity) FROM tracks")
        stats['avg_popularity'] = round(cursor.fetchone()[0] or 0, 2)

        # Most popular track
        cursor.execute("""
            SELECT name, popularity FROM tracks
            ORDER BY popularity DESC LIMIT 1
        """)
        result = cursor.fetchone()
        stats['most_popular_track'] = {"name": result[0], "popularity": result[1]} if result else None

        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/update-tracks', methods=['POST'])
def update_tracks():
    connection = None
    cursor = None
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Get all tracks from database
        cursor.execute("SELECT track_id, spotify_id FROM tracks")
        tracks = cursor.fetchall()

        updated_count = 0

        for track in tracks:
            try:
                # Fetch latest track data from Spotify
                track_data = sp.track(track['spotify_id'])

                # Fetch latest audio features
                audio_features = sp.audio_features([track['spotify_id']])[0]

                # Update track information
                cursor.execute("""
                    UPDATE tracks
                    SET popularity = %s, duration_ms = %s
                    WHERE track_id = %s
                """, (
                    track_data['popularity'],
                    track_data['duration_ms'],
                    track['track_id']
                ))

                # Update audio features if available
                if audio_features:
                    cursor.execute("""
                        UPDATE audio_features
                        SET danceability = %s, energy = %s, key = %s, loudness = %s,
                            mode = %s, speechiness = %s, acousticness = %s,
                            instrumentalness = %s, liveness = %s, valence = %s,
                            tempo = %s, duration_ms = %s, time_signature = %s
                        WHERE track_id = %s
                    """, (
                        audio_features.get('danceability'),
                        audio_features.get('energy'),
                        audio_features.get('key'),
                        audio_features.get('loudness'),
                        audio_features.get('mode'),
                        audio_features.get('speechiness'),
                        audio_features.get('acousticness'),
                        audio_features.get('instrumentalness'),
                        audio_features.get('liveness'),
                        audio_features.get('valence'),
                        audio_features.get('tempo'),
                        audio_features.get('duration_ms'),
                        audio_features.get('time_signature'),
                        track['track_id']
                    ))

                updated_count += 1

            except Exception as e:
                print(f"Error updating track {track['spotify_id']}: {e}")
                continue

        connection.commit()
        return jsonify({"message": "Tracks updated successfully", "updated_count": updated_count})

    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/recommendations/<track_id>', methods=['GET'])
def get_recommendations(track_id):
    connection = None
    cursor = None
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Get audio features of the input track
        cursor.execute("""
            SELECT af.* FROM audio_features af
            JOIN tracks t ON af.track_id = t.track_id
            WHERE t.spotify_id = %s
        """, (track_id,))

        input_features = cursor.fetchone()
        if not input_features:
            return jsonify({"error": "Track not found or no audio features available"}), 404

        # Find similar tracks based on audio features
        cursor.execute("""
            SELECT t.name, ar.name as artist, af.*
            FROM audio_features af
            JOIN tracks t ON af.track_id = t.track_id
            JOIN artists ar ON t.artist_id = ar.artist_id
            WHERE af.track_id != %s
            ORDER BY (
                ABS(af.danceability - %s) +
                ABS(af.energy - %s) +
                ABS(af.valence - %s) +
                ABS(af.tempo - %s) / 100
            ) ASC
            LIMIT 5
        """, (
            input_features['track_id'],
            input_features['danceability'],
            input_features['energy'],
            input_features['valence'],
            input_features['tempo']
        ))

        recommendations = cursor.fetchall()
        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/export-analysis', methods=['POST'])
def export_analysis():
    try:
        data = request.get_json()
        analysis_type = data.get('type')
        analysis_data = data.get('data')

        if not analysis_type or not analysis_data:
            return jsonify({"error": "Missing analysis type or data"}), 400

        connection = create_connection()
        cursor = connection.cursor()

        if analysis_type == 'track':
            # Insert single track analysis
            track_data = analysis_data

            # Get or create artist
            artist_id = get_or_create_artist(track_data['artists'][0]['name'], cursor)

            # Get or create album
            album_id = get_or_create_album(track_data['album']['name'], artist_id, cursor)

            # Insert track
            cursor.execute("""
                INSERT INTO tracks (name, artist_id, album_id, popularity, duration_ms, spotify_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE popularity = VALUES(popularity)
            """, (
                track_data['name'],
                artist_id,
                album_id,
                track_data['popularity'],
                track_data['duration_ms'],
                track_data['id']
            ))

            track_id = cursor.lastrowid or cursor.execute("SELECT track_id FROM tracks WHERE spotify_id = %s", (track_data['id'],)) or cursor.fetchone()[0]

            # Insert audio features if available
            if track_data.get('audio_features'):
                audio_features = track_data['audio_features']
                cursor.execute("""
                    INSERT INTO audio_features
                    (track_id, danceability, energy, key, loudness, mode, speechiness,
                     acousticness, instrumentalness, liveness, valence, tempo, duration_ms,
                     time_signature)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE track_id = track_id
                """, (
                    track_id,
                    audio_features.get('danceability'),
                    audio_features.get('energy'),
                    audio_features.get('key'),
                    audio_features.get('loudness'),
                    audio_features.get('mode'),
                    audio_features.get('speechiness'),
                    audio_features.get('acousticness'),
                    audio_features.get('instrumentalness'),
                    audio_features.get('liveness'),
                    audio_features.get('valence'),
                    audio_features.get('tempo'),
                    audio_features.get('duration_ms'),
                    audio_features.get('time_signature')
                ))

        elif analysis_type == 'playlist':
            # Insert playlist tracks analysis
            tracks_data = analysis_data.get('tracks', [])

            for track_data in tracks_data:
                # Get or create artist
                artist_id = get_or_create_artist(track_data['artists'][0]['name'], cursor)

                # Get or create album
                album_id = get_or_create_album(track_data['album']['name'], artist_id, cursor)

                # Insert track
                cursor.execute("""
                    INSERT INTO tracks (name, artist_id, album_id, popularity, duration_ms, spotify_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE popularity = VALUES(popularity)
                """, (
                    track_data['name'],
                    artist_id,
                    album_id,
                    track_data['popularity'],
                    track_data['duration_ms'],
                    track_data['id']
                ))

                track_id = cursor.lastrowid or cursor.execute("SELECT track_id FROM tracks WHERE spotify_id = %s", (track_data['id'],)) or cursor.fetchone()[0]

                # Insert audio features if available
                if track_data.get('audio_features'):
                    audio_features = track_data['audio_features']
                    cursor.execute("""
                        INSERT INTO audio_features
                        (track_id, danceability, energy, key, loudness, mode, speechiness,
                         acousticness, instrumentalness, liveness, valence, tempo, duration_ms,
                         time_signature)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE track_id = track_id
                    """, (
                        track_id,
                        audio_features.get('danceability'),
                        audio_features.get('energy'),
                        audio_features.get('key'),
                        audio_features.get('loudness'),
                        audio_features.get('mode'),
                        audio_features.get('speechiness'),
                        audio_features.get('acousticness'),
                        audio_features.get('instrumentalness'),
                        audio_features.get('liveness'),
                        audio_features.get('valence'),
                        audio_features.get('tempo'),
                        audio_features.get('duration_ms'),
                        audio_features.get('time_signature')
                    ))

        connection.commit()
        return jsonify({"message": f"{analysis_type.capitalize()} analysis data exported successfully"}), 200

    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)

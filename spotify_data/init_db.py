import mysql.connector
import os

def init_database():
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='P@ssw0rd'
        )
        cursor = connection.cursor()

        # Read and execute the SQL file
        with open('spotify.sql', 'r', encoding='utf-8') as file:
            sql_content = file.read()

        # Split SQL commands and execute them
        sql_commands = sql_content.split(';')
        for command in sql_commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    print(f"Executed: {command[:50]}...")
                except Exception as e:
                    print(f"Error executing command: {e}")
                    print(f"Command was: {command}")

        connection.commit()
        print("Database initialized successfully!")

        # Verify data insertion
        cursor.execute("USE spotify_db")
        cursor.execute("SELECT COUNT(*) FROM tracks")
        track_count = cursor.fetchone()[0]
        print(f"Inserted {track_count} tracks")

        cursor.execute("SELECT COUNT(*) FROM artists")
        artist_count = cursor.fetchone()[0]
        print(f"Inserted {artist_count} artists")

        cursor.execute("SELECT COUNT(*) FROM audio_features")
        features_count = cursor.fetchone()[0]
        print(f"Inserted {features_count} audio features")

    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    init_database()

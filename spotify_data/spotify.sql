-- Spotify Analytics Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS spotify_db;
USE spotify_db;

-- Artists table
CREATE TABLE IF NOT EXISTS artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Albums table
CREATE TABLE IF NOT EXISTS albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

-- Tracks table
CREATE TABLE IF NOT EXISTS tracks (
    track_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    artist_id INT,
    album_id INT,
    popularity INT,
    duration_ms INT,
    spotify_id VARCHAR(50) UNIQUE,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES albums(album_id)
);

-- Audio features table
CREATE TABLE IF NOT EXISTS audio_features (
    track_id INT PRIMARY KEY,
    danceability DECIMAL(3,2),
    energy DECIMAL(3,2),
    key INT,
    loudness DECIMAL(4,2),
    mode INT,
    speechiness DECIMAL(3,2),
    acousticness DECIMAL(3,2),
    instrumentalness DECIMAL(3,2),
    liveness DECIMAL(3,2),
    valence DECIMAL(3,2),
    tempo DECIMAL(5,2),
    duration_ms INT,
    time_signature INT,
    FOREIGN KEY (track_id) REFERENCES tracks(track_id)
);

-- Insert sample artists
INSERT IGNORE INTO artists (name) VALUES
('Ed Sheeran'),
('Lewis Capaldi'),
('The Weeknd'),
('Clean Bandit'),
('Dua Lipa'),
('Harry Styles'),
('Olivia Rodrigo');

-- Insert sample albums
INSERT IGNORE INTO albums (name, artist_id) VALUES
('÷ (Divide)', (SELECT artist_id FROM artists WHERE name = 'Ed Sheeran')),
('Divinely Uninspired To A Hellish Extent', (SELECT artist_id FROM artists WHERE name = 'Lewis Capaldi')),
('After Hours', (SELECT artist_id FROM artists WHERE name = 'The Weeknd')),
('New Eyes', (SELECT artist_id FROM artists WHERE name = 'Clean Bandit')),
('Future Nostalgia', (SELECT artist_id FROM artists WHERE name = 'Dua Lipa')),
('Fine Line', (SELECT artist_id FROM artists WHERE name = 'Harry Styles')),
('Harry''s House', (SELECT artist_id FROM artists WHERE name = 'Harry Styles')),
('SOUR', (SELECT artist_id FROM artists WHERE name = 'Olivia Rodrigo'));

-- Insert sample tracks
INSERT IGNORE INTO tracks (name, artist_id, album_id, popularity, duration_ms, spotify_id) VALUES
('Shape of You', (SELECT artist_id FROM artists WHERE name = 'Ed Sheeran'), (SELECT album_id FROM albums WHERE name = '÷ (Divide)'), 85, 233712, '4iV5W9uYEdYUVa79Axb7Rh'),
('Perfect', (SELECT artist_id FROM artists WHERE name = 'Ed Sheeran'), (SELECT album_id FROM albums WHERE name = '÷ (Divide)'), 87, 263400, '0tgVpDi06FyKpA1z0VMD4v'),
('Someone You Loved', (SELECT artist_id FROM artists WHERE name = 'Lewis Capaldi'), (SELECT album_id FROM albums WHERE name = 'Divinely Uninspired To A Hellish Extent'), 88, 182160, '1Je1IMUlBXcx1Fz0WE7oPT'),
('Blinding Lights', (SELECT artist_id FROM artists WHERE name = 'The Weeknd'), (SELECT album_id FROM albums WHERE name = 'After Hours'), 91, 200040, '4uLU6hMCjMI75M1A2tKUQC'),
('Rather Be', (SELECT artist_id FROM artists WHERE name = 'Clean Bandit'), (SELECT album_id FROM albums WHERE name = 'New Eyes'), 78, 227833, '11dFghVXANMlKmJXsNCbNl'),
('Levitating', (SELECT artist_id FROM artists WHERE name = 'Dua Lipa'), (SELECT album_id FROM albums WHERE name = 'Future Nostalgia'), 83, 203064, '0VjIjW4GlUZAMYd2vXMi3b'),
('Watermelon Sugar', (SELECT artist_id FROM artists WHERE name = 'Harry Styles'), (SELECT album_id FROM albums WHERE name = 'Fine Line'), 82, 174000, '7qiZfU4dY1lWllzX7mPBI3'),
('As It Was', (SELECT artist_id FROM artists WHERE name = 'Harry Styles'), (SELECT album_id FROM albums WHERE name = 'Harry''s House'), 92, 167303, '4Dvkj6JhhA12EX05fT7y2e'),
('Good 4 U', (SELECT artist_id FROM artists WHERE name = 'Olivia Rodrigo'), (SELECT album_id FROM albums WHERE name = 'SOUR'), 85, 178146, '5ChkMS8OtdzJeqyybCc9R5'),
('drivers license', (SELECT artist_id FROM artists WHERE name = 'Olivia Rodrigo'), (SELECT album_id FROM albums WHERE name = 'SOUR'), 84, 242014, '6habFhsOp2NvshLv26DqMb');

-- Insert sample audio features
INSERT IGNORE INTO audio_features (track_id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature) VALUES
((SELECT track_id FROM tracks WHERE spotify_id = '4iV5W9uYEdYUVa79Axb7Rh'), 0.83, 0.65, 1, -3.18, 0, 0.08, 0.58, 0.00, 0.09, 0.93, 95.98, 233712, 4),
((SELECT track_id FROM tracks WHERE spotify_id = '0tgVpDi06FyKpA1z0VMD4v'), 0.60, 0.45, 8, -6.66, 1, 0.03, 0.16, 0.00, 0.11, 0.17, 95.05, 263400, 3),
((SELECT track_id FROM tracks WHERE spotify_id = '1Je1IMUlBXcx1Fz0WE7oPT'), 0.50, 0.41, 1, -5.68, 1, 0.03, 0.74, 0.00, 0.11, 0.45, 109.95, 182160, 4),
((SELECT track_id FROM tracks WHERE spotify_id = '4uLU6hMCjMI75M1A2tKUQC'), 0.51, 0.73, 1, -5.93, 1, 0.06, 0.00, 0.00, 0.09, 0.33, 171.00, 200040, 4),
((SELECT track_id FROM tracks WHERE spotify_id = '11dFghVXANMlKmJXsNCbNl'), 0.80, 0.77, 11, -4.75, 0, 0.05, 0.19, 0.00, 0.15, 0.94, 120.94, 227833, 4),
((SELECT track_id FROM tracks WHERE spotify_id = '0VjIjW4GlUZAMYd2vXMi3b'), 0.70, 0.88, 6, -3.78, 0, 0.06, 0.05, 0.00, 0.16, 0.91, 103.02, 203064, 4),
((SELECT track_id FROM tracks WHERE spotify_id = '7qiZfU4dY1lWllzX7mPBI3'), 0.55, 0.82, 0, -4.21, 1, 0.05, 0.12, 0.00, 0.33, 0.55, 95.39, 174000, 4),
((SELECT track_id FROM tracks WHERE spotify_id = '4Dvkj6JhhA12EX05fT7y2e'), 0.52, 0.73, 6, -5.34, 0, 0.05, 0.34, 0.00, 0.31, 0.66, 173.93, 167303, 4),
((SELECT track_id FROM tracks WHERE spotify_id = '5ChkMS8OtdzJeqyybCc9R5'), 0.56, 0.66, 11, -5.01, 0, 0.15, 0.09, 0.00, 0.09, 0.68, 166.92, 178146, 4),
((SELECT track_id FROM tracks WHERE spotify_id = '6habFhsOp2NvshLv26DqMb'), 0.56, 0.43, 10, -8.37, 1, 0.06, 0.75, 0.00, 0.12, 0.22, 143.87, 242014, 4);

-- Create indexes for better performance
CREATE INDEX idx_tracks_artist_id ON tracks(artist_id);
CREATE INDEX idx_tracks_album_id ON tracks(album_id);
CREATE INDEX idx_tracks_popularity ON tracks(popularity DESC);
CREATE INDEX idx_albums_artist_id ON albums(artist_id);

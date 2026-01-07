# Spotify Analytics Dashboard

A full-stack web application for analyzing Spotify tracks and playlists with data visualization and database management.

## Features

- **Track Analysis**: Analyze individual Spotify tracks with metadata and audio features
- **Playlist Analysis**: Analyze entire playlists with aggregated statistics and charts
- **Audio Features**: View detailed audio features like danceability, energy, tempo, etc.
- **Data Visualization**: Interactive charts using Chart.js (bar charts, radar charts, doughnut charts)
- **Database Explorer**: Browse, search, sort, and export stored tracks
- **Recommendation Engine**: Get track recommendations based on audio features

## Tech Stack

### Backend
- **Flask**: REST API server
- **Spotipy**: Spotify Web API integration
- **MySQL**: Database for storing track data
- **Pandas**: Data processing

### Frontend
- **React**: User interface
- **Vite**: Build tool and dev server
- **Chart.js**: Data visualization
- **Axios**: HTTP client

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL Server
- Spotify Developer Account (for API credentials)

### 1. Database Setup
1. Start MySQL server
2. Create database: `CREATE DATABASE spotify_db;`
3. Run the SQL script: `mysql -u root -p spotify_db < spotify.sql`

### 2. Backend Setup
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Update Spotify credentials in `app.py`:
   ```python
   sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
       client_id='YOUR_CLIENT_ID',
       client_secret='YOUR_CLIENT_SECRET'
   ))
   ```

3. Update MySQL connection in `app.py` if needed

4. Run the Flask server:
   ```bash
   python app.py
   ```
   Server will start on http://127.0.0.1:5000

### 3. Frontend Setup
1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```
   Frontend will be available on http://localhost:5173

## API Endpoints

- `POST /api/analyze-track`: Analyze a single track from URL
- `POST /api/analyze-playlist`: Analyze a playlist from URL
- `GET /api/tracks`: Get all stored tracks
- `GET /api/stats`: Get database statistics
- `GET /api/recommendations/<track_id>`: Get track recommendations

## Usage

1. Open the React app in your browser
2. Paste a Spotify track or playlist URL
3. Click "Analyze Track" or "Analyze Playlist"
4. View detailed analytics, charts, and metadata
5. Explore stored tracks in the Database Explorer

## Project Structure

```
spotify_data/
├── app.py                 # Flask API server
├── spotify.sql           # Database schema
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
├── index.html           # React app entry
├── vite.config.js       # Vite configuration
├── src/
│   ├── main.jsx         # React app entry
│   ├── App.jsx          # Main React component
│   ├── index.css        # Global styles
│   └── components/      # React components
│       ├── LandingPage.jsx
│       ├── TrackOverview.jsx
│       ├── Analytics.jsx
│       ├── DatabaseExplorer.jsx
│       └── Navbar.jsx
└── README.md
```

## Database Schema

- **artists**: Artist information
- **albums**: Album information
- **tracks**: Track metadata
- **audio_features**: Detailed audio analysis
- **playlists**: Playlist information
- **playlist_tracks**: Playlist-track relationships

## Future Enhancements

- User authentication with Spotify OAuth
- Advanced recommendation algorithms
- Real-time playlist updates
- Mobile-responsive design improvements
- Export analytics reports

## License

MIT License

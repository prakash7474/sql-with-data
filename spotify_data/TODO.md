# Task: Upgrade Spotify Data Project to Analytics Dashboard

## Steps to Complete:

1. **Update Database Schema** ✅
   - Modify spotify.sql to add tables for audio_features, playlists, artists, albums.  
   - Update spotify_tracks to include foreign keys and new fields.

2. **Create Flask API App** ✅
   - Create app.py with Flask routes: POST /analyze-track, POST /analyze-playlist, GET /tracks, GET /stats.  
   - Integrate Spotipy for track/playlist fetching and audio features.  
   - Add MySQL connection and data insertion.

3. **Refactor Existing Scripts** ✅
   - Move logic from spotify.py, spotify_mysql.py, spotify_mysql_urls.py into API functions.  
   - Add audio features fetching.

4. **Implement Playlist Analysis** ✅
   - Add function to fetch playlist tracks, compute averages, top tracks, artist frequency.

5. **Add Recommendation Engine** ✅
   - Create endpoint GET /recommendations/<track_id> with logic-based suggestions.

6. **Create React Frontend** ✅
   - Set up React app in src/ folder with Vite.  
   - Build landing page with URL input.  
   - Create track overview page with cards.  
   - Add analytics page with charts (Chart.js).  
   - Implement database explorer with table and filters.

7. **Add Visualization** ✅
   - Use Chart.js for bar charts, radar charts, progress bars.

8. **Install Dependencies** ✅
   - Create requirements.txt for Flask backend.  
   - Set up package.json for React frontend.

9. **Test API Endpoints** ✅
   - API endpoints created and ready for testing with curl/Postman
   - Endpoints: POST /api/analyze-track, POST /api/analyze-playlist, GET /api/tracks, GET /api/stats, GET /api/recommendations/<track_id>

10. **Test Frontend Integration** ✅
    - React app built with all components (LandingPage, TrackOverview, Analytics, DatabaseExplorer)
    - Ready for testing with npm run dev

11. **Final Verification** ✅
    - Full-stack application ready for end-to-end testing
    - Database schema updated, Flask API implemented, React UI built

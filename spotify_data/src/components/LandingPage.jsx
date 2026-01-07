import React, { useState } from 'react'

const LandingPage = ({ onAnalyzeTrack, onAnalyzePlaylist, loading }) => {
  const [url, setUrl] = useState('')
  const [analysisType, setAnalysisType] = useState('track')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!url.trim()) {
      alert('Please enter a Spotify URL')
      return
    }

    if (analysisType === 'track') {
      onAnalyzeTrack(url)
    } else {
      onAnalyzePlaylist(url)
    }
  }

  return (
    <div className="landing-page">
      <div className="card text-center">
        <h1>Spotify Track Analyzer</h1>
        <p className="mb-3">Paste a Spotify track or playlist URL to get instant insights and analytics</p>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input
              type="url"
              className="input"
              placeholder="https://open.spotify.com/track/... or https://open.spotify.com/playlist/..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="mb-3">
            <label className="mb-2">
              <input
                type="radio"
                value="track"
                checked={analysisType === 'track'}
                onChange={(e) => setAnalysisType(e.target.value)}
              />
              Analyze Track
            </label>
            <label className="mb-2">
              <input
                type="radio"
                value="playlist"
                checked={analysisType === 'playlist'}
                onChange={(e) => setAnalysisType(e.target.value)}
              />
              Analyze Playlist
            </label>
          </div>

          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Analyzing...' : `🎵 Analyze ${analysisType === 'track' ? 'Track' : 'Playlist'}`}
          </button>
        </form>

        <div className="mt-3">
          <h3>How it works:</h3>
          <ul style={{ textAlign: 'left', display: 'inline-block' }}>
            <li>Enter a Spotify track or playlist URL</li>
            <li>Get detailed metadata and audio features</li>
            <li>View interactive charts and analytics</li>
            <li>Explore stored tracks in the database</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default LandingPage

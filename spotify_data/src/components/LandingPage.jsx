import React, { useState, useEffect } from 'react'

const LandingPage = ({ onAnalyzeTrack, onAnalyzePlaylist, loading }) => {
  const [url, setUrl] = useState('')
  const [analysisType, setAnalysisType] = useState('track')
  const [urlError, setUrlError] = useState('')

  // Automatically detect URL type and validate
  useEffect(() => {
    if (url.trim()) {
      const detectedType = detectUrlType(url)
      if (detectedType) {
        setAnalysisType(detectedType)
        setUrlError('')
      } else {
        setUrlError('Invalid Spotify URL. Please enter a valid Spotify track or playlist URL.')
      }
    } else {
      setUrlError('')
    }
  }, [url])

  const detectUrlType = (spotifyUrl) => {
    if (!spotifyUrl.includes('spotify.com')) {
      return null
    }

    if (spotifyUrl.includes('/track/')) {
      return 'track'
    } else if (spotifyUrl.includes('/playlist/')) {
      return 'playlist'
    }

    return null
  }

  const validateUrl = (spotifyUrl) => {
    const urlPattern = /^https:\/\/open\.spotify\.com\/(track|playlist)\/[a-zA-Z0-9]+/
    return urlPattern.test(spotifyUrl)
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    if (analysisType === 'static') {
      // For static data analysis, no URL validation needed
      onAnalyzeTrack({ source: 'static' })
      return
    }

    if (!url.trim()) {
      setUrlError('Please enter a Spotify URL')
      return
    }

    if (!validateUrl(url)) {
      setUrlError('Invalid Spotify URL format. Please check and try again.')
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
            {urlError && <div className="error-message" style={{ color: 'red', fontSize: '14px', marginTop: '5px' }}>{urlError}</div>}
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
            <label className="mb-2">
              <input
                type="radio"
                value="static"
                checked={analysisType === 'static'}
                onChange={(e) => setAnalysisType(e.target.value)}
              />
              Analyze Static Data
            </label>
          </div>

          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Analyzing...' : `🎵 Analyze ${analysisType === 'track' ? 'Track' : analysisType === 'playlist' ? 'Playlist' : 'Static Data'}`}
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

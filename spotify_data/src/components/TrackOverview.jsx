import React, { useState } from 'react'
import { Radar } from 'react-chartjs-2'
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js'

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

const TrackOverview = ({ track, onBack }) => {
  const [exportLoading, setExportLoading] = useState(false)

  if (!track) return <div>No track data available</div>

  const handleExport = async () => {
    setExportLoading(true)
    try {
      const response = await fetch('/api/export-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'track',
          data: track
        })
      })

      if (response.ok) {
        alert('Track analysis data exported successfully!')
      } else {
        const error = await response.json()
        alert(`Export failed: ${error.error}`)
      }
    } catch (error) {
      console.error('Export error:', error)
      alert('Export failed. Please try again.')
    }
    setExportLoading(false)
  }

  const formatDuration = (ms) => {
    const minutes = Math.floor(ms / 60000)
    const seconds = Math.floor((ms % 60000) / 1000)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  const getPopularityColor = (popularity) => {
    if (popularity >= 80) return '#1DB954'
    if (popularity >= 50) return '#FFA500'
    return '#FF6B6B'
  }

  const audioFeatures = track.audio_features
  const radarData = audioFeatures ? {
    labels: ['Danceability', 'Energy', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence'],
    datasets: [{
      label: 'Audio Features',
      data: [
        audioFeatures.danceability,
        audioFeatures.energy,
        audioFeatures.speechiness,
        audioFeatures.acousticness,
        audioFeatures.instrumentalness,
        audioFeatures.liveness,
        audioFeatures.valence
      ],
      backgroundColor: 'rgba(29, 185, 84, 0.2)',
      borderColor: '#1DB954',
      borderWidth: 2,
      pointBackgroundColor: '#1DB954'
    }]
  } : null

  const radarOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Audio Features Analysis' }
    },
    scales: {
      r: {
        beginAtZero: true,
        max: 1
      }
    }
  }

  return (
    <div className="track-overview">
      <button className="btn btn-secondary mb-3" onClick={onBack}>← Back to Home</button>
      <button
        className="btn btn-success mb-3"
        onClick={handleExport}
        disabled={exportLoading}
      >
        {exportLoading ? 'Exporting...' : '💾 Export Analysis'}
      </button>

      <div className="card">
        <div className="grid">
          <div>
            <img
              src={track.album?.images?.[0]?.url || '/placeholder-album.png'}
              alt="Album cover"
              style={{ width: '200px', height: '200px', objectFit: 'cover', borderRadius: '8px' }}
            />
          </div>
          <div>
            <h2>{track.name}</h2>
            <p className="mb-2"><strong>Artist:</strong> {track.artists?.[0]?.name || 'Unknown'}</p>
            <p className="mb-2"><strong>Album:</strong> {track.album?.name || 'Unknown'}</p>
            <p className="mb-2"><strong>Duration:</strong> {formatDuration(track.duration_ms)}</p>
            <div className="mb-2">
              <strong>Popularity:</strong> {track.popularity}/100
              <div style={{
                width: '100%',
                height: '10px',
                backgroundColor: '#333',
                borderRadius: '5px',
                marginTop: '5px'
              }}>
                <div style={{
                  width: `${track.popularity}%`,
                  height: '100%',
                  backgroundColor: getPopularityColor(track.popularity),
                  borderRadius: '5px'
                }}></div>
              </div>
            </div>
            <p><strong>Release Date:</strong> {track.album?.release_date || 'Unknown'}</p>
          </div>
        </div>
      </div>

      {audioFeatures && (
        <div className="card">
          <h3>Audio Features</h3>
          <div className="grid">
            <div>
              <p><strong>Tempo:</strong> {audioFeatures.tempo?.toFixed(1)} BPM</p>
              <p><strong>Key:</strong> {audioFeatures.key !== null ? audioFeatures.key : 'Unknown'}</p>
              <p><strong>Mode:</strong> {audioFeatures.mode === 1 ? 'Major' : 'Minor'}</p>
              <p><strong>Time Signature:</strong> {audioFeatures.time_signature}/4</p>
              <p><strong>Loudness:</strong> {audioFeatures.loudness?.toFixed(1)} dB</p>
            </div>
            <div style={{ height: '300px' }}>
              <Radar data={radarData} options={radarOptions} />
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <h3>Spotify Link</h3>
        <a href={track.external_urls?.spotify} target="_blank" rel="noopener noreferrer" className="btn">
          Open in Spotify
        </a>
      </div>
    </div>
  )
}

export default TrackOverview

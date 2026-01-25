import React, { useState, useEffect } from 'react'
import { Bar, Doughnut } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement)

const Analytics = ({ onBack, playlist }) => {
  const [stats, setStats] = useState(null)
  const [tracks, setTracks] = useState([])
  const [loading, setLoading] = useState(true)
  const [exportLoading, setExportLoading] = useState(false)

  useEffect(() => {
    fetchAnalyticsData()
  }, [])

  const fetchAnalyticsData = async () => {
    try {
      const [statsResponse, tracksResponse] = await Promise.all([
        fetch('/api/stats'),
        fetch('/api/tracks')
      ])

      const statsData = await statsResponse.json()
      const tracksData = await tracksResponse.json()

      setStats(statsData)
      setTracks(tracksData.tracks || [])
    } catch (error) {
      console.error('Error fetching analytics data:', error)
    }
    setLoading(false)
  }

  const handleNoteButton = async () => {
    try {
      // Update existing track data with latest information from Spotify
      const response = await fetch('/api/update-tracks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const result = await response.json()
        alert(`Data updated successfully! Updated ${result.updated_count} tracks.`)
        // Refresh the analytics data
        fetchAnalyticsData()
      } else {
        const error = await response.json()
        alert(`Error: ${error.error}`)
      }
    } catch (error) {
      console.error('Error updating data:', error)
      alert('Error updating data')
    }
  }

  const handleExportButton = () => {
    if (!stats || tracks.length === 0) {
      alert('No data available to export.')
      return
    }

    // Prepare CSV data
    const csvHeaders = ['Track Name', 'Artist', 'Album', 'Popularity', 'Duration (minutes)', 'Spotify ID']
    const csvRows = tracks.map(track => [
      track.name,
      track.artist,
      track.album,
      track.popularity,
      (track.duration_ms / 60000).toFixed(2),
      track.spotify_id
    ])

    // Add summary stats as additional rows
    csvRows.unshift(['Summary Stats', '', '', '', '', ''])
    csvRows.unshift(['Total Tracks', stats.total_tracks, '', '', '', ''])
    csvRows.unshift(['Total Artists', stats.total_artists, '', '', '', ''])
    csvRows.unshift(['Total Albums', stats.total_albums, '', '', '', ''])
    csvRows.unshift(['Average Popularity', stats.avg_popularity, '', '', '', ''])

    // Create CSV content
    const csvContent = [csvHeaders, ...csvRows].map(row => row.join(',')).join('\n')

    // Create and download the file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', 'spotify_analysis_data.csv')
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    // Insert data into representative format (e.g., append to existing CSV)
    const representativeData = csvContent
    const existingData = localStorage.getItem('spotify_representative_data') || ''
    const updatedData = existingData ? existingData + '\n\n' + representativeData : representativeData
    localStorage.setItem('spotify_representative_data', updatedData)

    alert('Data exported successfully and inserted into representative format!')
  }

  const handleExportPlaylist = async () => {
    if (!playlist || !playlist.tracks || playlist.tracks.length === 0) {
      alert('No playlist data available to export.')
      return
    }

    setExportLoading(true)
    try {
      const response = await fetch('/api/export-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'playlist',
          data: playlist.tracks
        })
      })

      if (response.ok) {
        alert('Playlist analysis data exported successfully!')
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

  if (loading) return <div className="text-center">Loading analytics...</div>
  if (!stats) return <div className="text-center">No data available. Please analyze some tracks first.</div>

  // Calculate additional analytics from tracks
  const totalDuration = tracks.reduce((sum, track) => sum + track.duration_ms, 0)
  const avgDuration = tracks.length > 0 ? totalDuration / tracks.length / 60000 : 0 // in minutes

  // Top 5 tracks by popularity
  const topTracks = tracks
    .sort((a, b) => b.popularity - a.popularity)
    .slice(0, 5)

  // Artist frequency
  const artistCount = {}
  tracks.forEach(track => {
    const artist = track.artist || 'Unknown'
    artistCount[artist] = (artistCount[artist] || 0) + 1
  })
  const topArtists = Object.entries(artistCount)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5)

  const popularityChartData = {
    labels: topTracks.map(track => track.name.substring(0, 20) + '...'),
    datasets: [{
      label: 'Popularity',
      data: topTracks.map(track => track.popularity),
      backgroundColor: '#1DB954',
      borderColor: '#1DB954',
      borderWidth: 1
    }]
  }

  const artistChartData = {
    labels: topArtists.map(([artist]) => artist.substring(0, 15) + '...'),
    datasets: [{
      data: topArtists.map(([, count]) => count),
      backgroundColor: ['#1DB954', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
      borderWidth: 1
    }]
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Top 5 Tracks by Popularity' }
    }
  }

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'right' },
      title: { display: true, text: 'Artist Distribution' }
    }
  }

  return (
    <div className="analytics">
      <button className="btn btn-secondary mb-3" onClick={onBack}>← Back to Home</button>
      <button className="btn btn-primary mb-3" onClick={handleNoteButton}>Note</button>
      <button className="btn btn-success mb-3" onClick={handleExportButton}>Export Data</button>
      {playlist && playlist.tracks && playlist.tracks.length > 0 && (
        <button
          className="btn btn-success mb-3"
          onClick={handleExportPlaylist}
          disabled={exportLoading}
        >
          {exportLoading ? 'Exporting...' : '💾 Export Playlist Analysis'}
        </button>
      )}

      <div className="card">
        <h2>Database Analytics</h2>
        <div className="grid">
          <div>
            <p><strong>Total Tracks:</strong> {stats.total_tracks}</p>
            <p><strong>Total Artists:</strong> {stats.total_artists}</p>
            <p><strong>Total Albums:</strong> {stats.total_albums}</p>
            <p><strong>Average Popularity:</strong> {stats.avg_popularity}/100</p>
            <p><strong>Total Duration:</strong> {(totalDuration / 3600000).toFixed(1)} hours</p>
            <p><strong>Average Duration:</strong> {avgDuration.toFixed(1)} minutes</p>
          </div>
          <div>
            {stats.most_popular_track && (
              <div>
                <p><strong>Most Popular Track:</strong></p>
                <p>{stats.most_popular_track.name} ({stats.most_popular_track.popularity}/100)</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {tracks.length > 0 && (
        <>
          <div className="grid">
            <div className="card">
              <h3>Top Tracks by Popularity</h3>
              <Bar data={popularityChartData} options={chartOptions} />
            </div>

            <div className="card">
              <h3>Artist Distribution</h3>
              <Doughnut data={artistChartData} options={doughnutOptions} />
            </div>
          </div>

          <div className="card">
            <h3>Top 5 Tracks</h3>
            <div className="grid">
              {topTracks.map((track, index) => (
                <div key={track.id} className="card">
                  <h4>{index + 1}. {track.name}</h4>
                  <p><strong>Artist:</strong> {track.artist}</p>
                  <p><strong>Album:</strong> {track.album}</p>
                  <p><strong>Popularity:</strong> {track.popularity}/100</p>
                  <p><strong>Duration:</strong> {(track.duration_ms / 60000).toFixed(1)} min</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {tracks.length === 0 && (
        <div className="card">
          <p className="text-center">No tracks in database. Please analyze some tracks or playlists first.</p>
        </div>
      )}
    </div>
  )
}

export default Analytics

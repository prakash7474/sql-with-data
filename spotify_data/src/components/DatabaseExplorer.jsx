import React, { useState, useEffect } from 'react'

const DatabaseExplorer = ({ onBack }) => {
  const [tracks, setTracks] = useState([])
  const [filteredTracks, setFilteredTracks] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('name')
  const [sortOrder, setSortOrder] = useState('asc')

  useEffect(() => {
    fetchTracks()
  }, [])

  useEffect(() => {
    filterAndSortTracks()
  }, [tracks, searchTerm, sortBy, sortOrder])

  const fetchTracks = async () => {
    try {
      const response = await fetch('/api/tracks')
      const data = await response.json()
      setTracks(data.tracks || [])
    } catch (error) {
      console.error('Error fetching tracks:', error)
    }
    setLoading(false)
  }

  const filterAndSortTracks = () => {
    let filtered = tracks.filter(track =>
      track.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      track.artist.toLowerCase().includes(searchTerm.toLowerCase()) ||
      track.album.toLowerCase().includes(searchTerm.toLowerCase())
    )

    filtered.sort((a, b) => {
      let aVal = a[sortBy]
      let bVal = b[sortBy]

      if (typeof aVal === 'string') {
        aVal = aVal.toLowerCase()
        bVal = bVal.toLowerCase()
      }

      if (sortOrder === 'asc') {
        return aVal > bVal ? 1 : -1
      } else {
        return aVal < bVal ? 1 : -1
      }
    })

    setFilteredTracks(filtered)
  }

  const exportToCSV = () => {
    const csvContent = [
      ['Name', 'Artist', 'Album', 'Popularity', 'Duration (min)'],
      ...filteredTracks.map(track => [
        track.name,
        track.artist,
        track.album,
        track.popularity,
        (track.duration_ms / 60000).toFixed(2)
      ])
    ].map(row => row.join(',')).join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'spotify_tracks.csv'
    a.click()
    window.URL.revokeObjectURL(url)
  }

  const deleteTrack = async (trackId) => {
    if (!confirm('Are you sure you want to delete this track?')) return

    try {
      const response = await fetch(`/api/tracks/${trackId}`, { method: 'DELETE' })
      if (response.ok) {
        setTracks(tracks.filter(track => track.id !== trackId))
      } else {
        alert('Error deleting track')
      }
    } catch (error) {
      console.error('Error deleting track:', error)
      alert('Error deleting track')
    }
  }

  if (loading) return <div className="text-center">Loading tracks...</div>

  return (
    <div className="database-explorer">
      <button className="btn btn-secondary mb-3" onClick={onBack}>← Back to Home</button>

      <div className="card">
        <h2>Database Explorer</h2>
        <div className="flex mb-3">
          <input
            type="text"
            className="input"
            placeholder="Search tracks, artists, or albums..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ flex: 1 }}
          />
          <select
            className="input"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            style={{ width: '150px' }}
          >
            <option value="name">Sort by Name</option>
            <option value="artist">Sort by Artist</option>
            <option value="album">Sort by Album</option>
            <option value="popularity">Sort by Popularity</option>
          </select>
          <button
            className="btn btn-secondary"
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
          >
            {sortOrder === 'asc' ? '↑' : '↓'}
          </button>
          <button className="btn" onClick={exportToCSV}>Export CSV</button>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#333' }}>
                <th style={{ padding: '10px', textAlign: 'left' }}>Name</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Artist</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Album</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Popularity</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Duration</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTracks.map(track => (
                <tr key={track.id} style={{ borderBottom: '1px solid #444' }}>
                  <td style={{ padding: '10px' }}>{track.name}</td>
                  <td style={{ padding: '10px' }}>{track.artist}</td>
                  <td style={{ padding: '10px' }}>{track.album}</td>
                  <td style={{ padding: '10px' }}>{track.popularity}/100</td>
                  <td style={{ padding: '10px' }}>{(track.duration_ms / 60000).toFixed(1)} min</td>
                  <td style={{ padding: '10px' }}>
                    <button
                      className="btn btn-secondary"
                      onClick={() => deleteTrack(track.id)}
                      style={{ fontSize: '0.8rem', padding: '0.25rem 0.5rem' }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredTracks.length === 0 && (
          <p className="text-center mt-3">No tracks found matching your search.</p>
        )}
      </div>
    </div>
  )
}

export default DatabaseExplorer

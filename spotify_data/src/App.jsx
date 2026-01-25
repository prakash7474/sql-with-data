import { useState } from 'react'
import LandingPage from './components/LandingPage'
import TrackOverview from './components/TrackOverview'
import Analytics from './components/Analytics'
import DatabaseExplorer from './components/DatabaseExplorer'
import Navbar from './components/Navbar'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('landing')
  const [trackData, setTrackData] = useState(null)
  const [playlistData, setPlaylistData] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyzeTrack = async (input) => {
    setLoading(true)
    try {
      let requestBody

      if (typeof input === 'string') {
        // URL-based analysis
        requestBody = { url: input }
      } else if (typeof input === 'object' && input.source === 'static') {
        // Static data analysis
        requestBody = { source: 'static' }
      } else {
        throw new Error('Invalid input format')
      }

      const response = await fetch('/api/analyze-track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      if (data.type === 'static_analysis') {
        // For static analysis, show analytics page instead of track overview
        setPlaylistData(data)
        setCurrentPage('analytics')
      } else {
        // Regular track analysis
        setTrackData(data)
        setCurrentPage('overview')
      }
    } catch (error) {
      console.error('Error analyzing track:', error)
      alert('Error analyzing track. Please check the input and try again.')
    }
    setLoading(false)
  }

  const handleAnalyzePlaylist = async (url) => {
    setLoading(true)
    try {
      const response = await fetch('/api/analyze-playlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      const data = await response.json()
      setPlaylistData(data)
      setCurrentPage('analytics')
    } catch (error) {
      console.error('Error analyzing playlist:', error)
      alert('Error analyzing playlist. Please check the URL and try again.')
    }
    setLoading(false)
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'landing':
        return (
          <LandingPage
            onAnalyzeTrack={handleAnalyzeTrack}
            onAnalyzePlaylist={handleAnalyzePlaylist}
            loading={loading}
          />
        )
      case 'overview':
        return <TrackOverview track={trackData} onBack={() => setCurrentPage('landing')} />
      case 'analytics':
        return <Analytics playlist={playlistData} onBack={() => setCurrentPage('landing')} />
      case 'explorer':
        return <DatabaseExplorer onBack={() => setCurrentPage('landing')} />
      default:
        return <LandingPage onAnalyzeTrack={handleAnalyzeTrack} onAnalyzePlaylist={handleAnalyzePlaylist} loading={loading} />
    }
  }

  return (
    <div className="App">
      <Navbar currentPage={currentPage} onNavigate={setCurrentPage} />
      <main className="container">
        {renderPage()}
      </main>
    </div>
  )
}

export default App

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

  const handleAnalyzeTrack = async (url) => {
    setLoading(true)
    try {
      const response = await fetch('/api/analyze-track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      const data = await response.json()
      setTrackData(data)
      setCurrentPage('overview')
    } catch (error) {
      console.error('Error analyzing track:', error)
      alert('Error analyzing track. Please check the URL and try again.')
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

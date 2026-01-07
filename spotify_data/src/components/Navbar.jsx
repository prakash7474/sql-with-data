import React from 'react'

const Navbar = ({ currentPage, onNavigate }) => {
  return (
    <nav className="navbar">
      <div className="nav-brand" onClick={() => onNavigate('landing')}>
        🎵 Spotify Analytics
      </div>
      <div className="nav-links">
        <button
          className={currentPage === 'landing' ? 'active' : ''}
          onClick={() => onNavigate('landing')}
        >
          Home
        </button>
        <button
          className={currentPage === 'explorer' ? 'active' : ''}
          onClick={() => onNavigate('explorer')}
        >
          Database
        </button>
      </div>
    </nav>
  )
}

export default Navbar

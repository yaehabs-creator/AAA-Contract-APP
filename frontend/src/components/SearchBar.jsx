import React from 'react'
import './SearchBar.css'

function SearchBar({ searchTerm, onSearchChange, disabled }) {
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search by clause number or text…"
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
        disabled={disabled}
        className="search-input"
      />
    </div>
  )
}

export default SearchBar

import React, { useState, useEffect } from 'react'
import './App.css'
import UploadSection from './components/UploadSection'
import SearchBar from './components/SearchBar'
import TabNavigation from './components/TabNavigation'
import ClauseList from './components/ClauseList'
import ClauseDetail from './components/ClauseDetail'
import ComparisonView from './components/ComparisonView'
import { getClauses, getComparison, getTimeFrames } from './services/api'

function App() {
  const [activeTab, setActiveTab] = useState('general')
  const [searchTerm, setSearchTerm] = useState('')
  const [clauses, setClauses] = useState([])
  const [selectedClause, setSelectedClause] = useState(null)
  const [loading, setLoading] = useState(false)
  const [comparison, setComparison] = useState([])
  const [uploading, setUploading] = useState(false)

  // Fetch clauses based on active tab and search
  useEffect(() => {
    setSelectedClause(null) // Clear selection when tab changes
    fetchClauses()
  }, [activeTab, searchTerm])

  const fetchClauses = async () => {
    setLoading(true)
    try {
      let data
      if (activeTab === 'comparison') {
        data = await getComparison()
        setComparison(data.comparison || [])
      } else if (activeTab === 'timeframes') {
        data = await getTimeFrames()
        setClauses(data.clauses || [])
      } else {
        const clauseType = activeTab === 'general' ? 'General Condition' : 
                          activeTab === 'particular' ? 'Particular Condition' : null
        data = await getClauses(clauseType, searchTerm)
        setClauses(data.clauses || [])
      }
    } catch (error) {
      console.error('Error fetching clauses:', error)
      alert('Error loading clauses. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleUploadComplete = () => {
    setUploading(false)
    setSelectedClause(null)
    setActiveTab('general')
    // Refresh clauses after upload
    fetchClauses()
  }

  const handleUploadStart = () => {
    setUploading(true)
  }

  const handleClauseSelect = (clause) => {
    setSelectedClause(clause)
  }

  return (
    <div className="app">
      {/* Top Bar */}
      <header className="top-bar">
        <h1 className="app-title">AAA</h1>
        <SearchBar 
          searchTerm={searchTerm} 
          onSearchChange={setSearchTerm}
          disabled={activeTab === 'comparison'}
        />
      </header>

      <div className="app-content">
        {/* Left Side - Upload Section */}
        <aside className="sidebar">
          <UploadSection 
            onUploadComplete={handleUploadComplete}
            onUploadStart={handleUploadStart}
            uploading={uploading}
          />
        </aside>

        {/* Main Content Area */}
        <main className="main-content">
          <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab} />
          
          {loading ? (
            <div className="loading">Loading...</div>
          ) : activeTab === 'comparison' ? (
            <ComparisonView comparison={comparison} />
          ) : (
            <div className="content-grid">
              <div className="clause-list-container">
                <ClauseList 
                  clauses={clauses}
                  activeTab={activeTab}
                  onClauseSelect={handleClauseSelect}
                  selectedClauseId={selectedClause?.id}
                />
              </div>
              {selectedClause && (
                <div className="clause-detail-container">
                  <ClauseDetail clause={selectedClause} />
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default App

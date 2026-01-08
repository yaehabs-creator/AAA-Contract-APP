import React from 'react'
import './ClauseList.css'

function ClauseList({ clauses, activeTab, onClauseSelect, selectedClauseId }) {
  if (clauses.length === 0) {
    return (
      <div className="clause-list empty">
        <p>No clauses found. Upload a contract to get started.</p>
      </div>
    )
  }

  return (
    <div className="clause-list">
      {clauses.map(clause => (
        <div
          key={clause.id}
          className={`clause-item ${selectedClauseId === clause.id ? 'selected' : ''}`}
          onClick={() => onClauseSelect(clause)}
        >
          <div className="clause-header">
            <span className="clause-number">
              {clause.clause_number || 'N/A'}
            </span>
            <span className={`clause-type-badge ${clause.clause_type?.toLowerCase().replace(' ', '-') || 'unknown'}`}>
              {clause.clause_type || 'Unknown'}
            </span>
          </div>
          {clause.clause_title && (
            <div className="clause-title">{clause.clause_title}</div>
          )}
          {clause.analysis_summary && (
            <div className="clause-summary">
              {clause.analysis_summary.substring(0, 150)}...
            </div>
          )}
          {activeTab === 'timeframes' && clause.time_frames_raw && (
            <div className="clause-timeframes-preview">
              ⏱️ {clause.time_frames_raw.substring(0, 100)}...
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

export default ClauseList

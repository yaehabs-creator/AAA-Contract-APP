import React from 'react'
import './ClauseDetail.css'

function ClauseDetail({ clause }) {
  if (!clause) {
    return (
      <div className="clause-detail">
        <p>Select a clause to view details</p>
      </div>
    )
  }

  return (
    <div className="clause-detail">
      <div className="detail-header">
        <div className="detail-title-section">
          <h2>Clause {clause.clause_number || 'N/A'}</h2>
          {clause.clause_title && (
            <h3 className="detail-title">{clause.clause_title}</h3>
          )}
        </div>
        <div className="detail-meta">
          <span className={`type-badge ${clause.clause_type?.toLowerCase().replace(' ', '-') || 'unknown'}`}>
            {clause.clause_type || 'Unknown'}
          </span>
          {clause.section_name && (
            <span className="section-name">{clause.section_name}</span>
          )}
        </div>
      </div>

      <div className="detail-section">
        <h4>Original Clause Text (unchanged from contract)</h4>
        <div className="original-text">
          <pre>{clause.full_text_original || 'No text available'}</pre>
        </div>
      </div>
      
      {clause.full_text_cleaned && clause.full_text_cleaned !== clause.full_text_original && (
        <div className="detail-section">
          <h4>Cleaned Text (spacing fixes only)</h4>
          <div className="cleaned-text">
            <pre>{clause.full_text_cleaned}</pre>
          </div>
        </div>
      )}

      {clause.analysis_summary && (
        <div className="detail-section">
          <h4>Analysis Summary</h4>
          <div className="detail-content">
            {clause.analysis_summary}
          </div>
        </div>
      )}

      {clause.time_frames_raw && (
        <div className="detail-section time-section">
          <h4>⏱️ Time Frames & Deadlines</h4>
          <div className="detail-content">
            <div className="time-frames-raw">
              <strong>Raw time expressions:</strong> {clause.time_frames_raw}
            </div>
            {clause.time_frames_explained && (
              <div className="time-frames-explained">
                <strong>Explanation:</strong>
                <pre>{clause.time_frames_explained}</pre>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default ClauseDetail

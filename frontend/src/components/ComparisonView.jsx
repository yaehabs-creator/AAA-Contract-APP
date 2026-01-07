import React, { useState } from 'react'
import './ComparisonView.css'
import ClauseDetail from './ClauseDetail'

function ComparisonView({ comparison }) {
  const [selectedClause, setSelectedClause] = useState(null)

  if (!comparison || comparison.length === 0) {
    return (
      <div className="comparison-view empty">
        <p>No comparison data available. Upload a contract with both General and Particular Conditions.</p>
      </div>
    )
  }

  return (
    <div className="comparison-container">
      <div className="comparison-table-container">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Topic / Clause Title</th>
              <th>General Condition</th>
              <th>Particular Condition</th>
              <th>Comment / Difference / Extra Risk</th>
            </tr>
          </thead>
          <tbody>
            {comparison.map((item, idx) => (
              <tr key={idx}>
                <td className="topic-cell">
                  <strong>{item.topic}</strong>
                </td>
                <td className="general-cell">
                  {item.general_clause ? (
                    <div 
                      className="clause-link"
                      onClick={() => {
                        // You would fetch the full clause here
                        // For now, we'll show a message
                        alert('Click to view full clause details')
                      }}
                    >
                      <div className="clause-ref">
                        Clause {item.general_clause.clause_number || 'N/A'}
                      </div>
                      {item.general_clause.clause_title && (
                        <div className="clause-title-small">
                          {item.general_clause.clause_title}
                        </div>
                      )}
                      {item.general_clause.summary && (
                        <div className="clause-summary-small">
                          {item.general_clause.summary}
                        </div>
                      )}
                    </div>
                  ) : (
                    <span className="no-clause">—</span>
                  )}
                </td>
                <td className="particular-cell">
                  {item.particular_clause ? (
                    <div className="clause-link">
                      <div className="clause-ref">
                        Clause {item.particular_clause.clause_number || 'N/A'}
                      </div>
                      {item.particular_clause.clause_title && (
                        <div className="clause-title-small">
                          {item.particular_clause.clause_title}
                        </div>
                      )}
                      {item.particular_clause.summary && (
                        <div className="clause-summary-small">
                          {item.particular_clause.summary}
                        </div>
                      )}
                    </div>
                  ) : (
                    <span className="no-clause">—</span>
                  )}
                </td>
                <td className="comment-cell">
                  <div className="comment-text">
                    {item.comment || '—'}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {selectedClause && (
        <div className="comparison-detail">
          <ClauseDetail clause={selectedClause} />
        </div>
      )}
    </div>
  )
}

export default ComparisonView

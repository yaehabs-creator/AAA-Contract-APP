import React from 'react'
import './TabNavigation.css'

function TabNavigation({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'general', label: 'General Conditions' },
    { id: 'particular', label: 'Particular Conditions' },
    { id: 'comparison', label: 'Comparison' },
    { id: 'timeframes', label: 'Time Frames & Deadlines' },
  ]

  return (
    <div className="tab-navigation">
      {tabs.map(tab => (
        <button
          key={tab.id}
          className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => setActiveTab(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  )
}

export default TabNavigation

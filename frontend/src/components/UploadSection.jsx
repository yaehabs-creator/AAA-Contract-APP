import React, { useRef, useState } from 'react'
import './UploadSection.css'
import { uploadContract } from '../services/api'

function UploadSection({ onUploadComplete, onUploadStart, uploading }) {
  const fileInputRef = useRef(null)
  const [dragActive, setDragActive] = useState(false)
  const [uploadStatus, setUploadStatus] = useState('')

  const handleFileSelect = async (file) => {
    if (!file || !file.name.endsWith('.pdf')) {
      alert('Please select a PDF file')
      return
    }

    onUploadStart()
    setUploadStatus('Uploading and processing contract...')

    try {
      const result = await uploadContract(file)
      setUploadStatus(`Success! Processed ${result.clauses_count} clauses.`)
      setTimeout(() => {
        setUploadStatus('')
        onUploadComplete()
      }, 2000)
    } catch (error) {
      setUploadStatus('Error: ' + (error.response?.data?.detail || error.message))
      onUploadStart(false)
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0])
    }
  }

  return (
    <div className="upload-section">
      <h2>Upload Contract</h2>
      <div
        className={`upload-area ${dragActive ? 'drag-active' : ''} ${uploading ? 'uploading' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {uploading ? (
          <div className="upload-status">
            <div className="spinner"></div>
            <p>{uploadStatus || 'Processing...'}</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📄</div>
            <p>Drag and drop your PDF contract here</p>
            <p className="upload-hint">or</p>
            <button
              className="browse-button"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
            >
              Browse Files
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleChange}
              style={{ display: 'none' }}
            />
          </>
        )}
      </div>
      {uploadStatus && !uploading && (
        <div className="upload-message">{uploadStatus}</div>
      )}
    </div>
  )
}

export default UploadSection

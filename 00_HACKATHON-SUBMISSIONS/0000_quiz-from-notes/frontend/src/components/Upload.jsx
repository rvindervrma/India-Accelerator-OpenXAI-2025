import { useState } from 'react'
import { uploadPdf } from '../services/api'

export default function Upload({ onUploaded }) {
  const [file, setFile] = useState(null)
  const [busy, setBusy] = useState(false)
  const [meta, setMeta] = useState(null)
  const [error, setError] = useState('')

  async function handleUpload() {
    if (!file) return
    setBusy(true)
    setError('')
    try {
      const res = await uploadPdf(file)
      setMeta(res)
      onUploaded?.(res.doc_id)
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="card">
      <h2>Upload your notes (PDF)</h2>
      <label>Select a PDF file</label>
      <input type="file" accept="application/pdf" onChange={e => setFile(e.target.files?.[0] || null)} />
      <div className="row mt-2">
        <button disabled={!file || busy} onClick={handleUpload}>{busy ? 'Uploading…' : 'Upload'}</button>
        {meta && <span className="badge">Pages: {meta.pages} • Chars: {meta.chars}</span>}
      </div>
      {error && <p style={{color:'#ff7b9b'}}>{error}</p>}
    </div>
  )
}

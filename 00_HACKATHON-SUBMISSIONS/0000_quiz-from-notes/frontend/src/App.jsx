import { useEffect, useMemo, useState } from 'react'
import Upload from './components/Upload'
import Quiz from './components/Quiz'
import Score from './components/Score'
import { generateQuiz, health } from './services/api'

export default function App() {
  const [docId, setDocId] = useState(null)
  const [questions, setQuestions] = useState([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [finalScore, setFinalScore] = useState(null)

  const model = useMemo(() => import.meta.env.VITE_DEFAULT_MODEL || 'llama3.1:8b', [])

  useEffect(() => { health().catch(()=>{}) }, [])

  async function startQuiz() {
    if (!docId) return
    setBusy(true)
    setError('')
    try {
      const res = await generateQuiz(docId, 8, model)
      setQuestions(res.questions || [])
    } catch (e) {
      setError(e.message)
    } finally {
      setBusy(false)
    }
  }

  function restart() {
    setDocId(null)
    setQuestions([])
    setFinalScore(null)
    setError('')
  }

  return (
    <div className="container">
      <div className="card" style={{marginBottom:16}}>
        <h1>Quiz from Notes</h1>
        <p className="text-muted">Upload your PDF, we generate MCQs using a local Ollama model, and you practice one question at a time with instant feedback.</p>
      </div>

      {!docId && (
        <Upload onUploaded={setDocId} />
      )}

      {docId && questions.length === 0 && finalScore === null && (
        <div className="card">
          <div className="row" style={{justifyContent:'space-between'}}>
            <div className="badge">doc: {docId.slice(0,8)}…</div>
            <div style={{fontSize:12}} className="text-muted">Model: {model}</div>
          </div>

          <label className="mt-3">Model</label>
          <input value={model} disabled />

          <div className="row mt-3">
            <button onClick={startQuiz} disabled={busy}>{busy ? 'Generating…' : 'Generate Quiz'}</button>
            <button onClick={restart} style={{background:'#26314f', color:'#eaf1ff'}}>Upload Another</button>
          </div>
          {error && <p style={{color:'#ff7b9b'}}>{error}</p>}
        </div>
      )}

      {questions.length > 0 && finalScore === null && (
        <Quiz questions={questions} onFinished={setFinalScore} />
      )}

      {finalScore !== null && (
        <Score score={finalScore} total={questions.length} onRestart={restart} />
      )}
    </div>
  )
}

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

export async function health() {
  const r = await fetch(`${API_BASE}/health`)
  return r.json()
}

export async function uploadPdf(file) {
  const form = new FormData()
  form.append('pdf', file)
  const r = await fetch(`${API_BASE}/upload`, { method: 'POST', body: form })
  if (!r.ok) throw new Error(`Upload failed: ${r.status}`)
  return r.json()
}

export async function generateQuiz(doc_id, num_questions = 8, model) {
  const r = await fetch(`${API_BASE}/generate-quiz`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ doc_id, num_questions, model })
  })
  if (!r.ok) throw new Error(`Quiz generation failed: ${r.status}`)
  return r.json()
}

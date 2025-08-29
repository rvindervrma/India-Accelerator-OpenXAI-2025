import { useMemo, useState } from 'react'

export default function Quiz({ questions, onFinished }) {
  const [idx, setIdx] = useState(0)
  const [selected, setSelected] = useState(null)
  const [revealed, setRevealed] = useState(false)
  const [score, setScore] = useState(0)

  const q = questions[idx]

  function choose(option) {
    if (revealed) return
    setSelected(option)
    const correct = option === q.answer
    if (correct) setScore(s => s + 1)
    setRevealed(true)
  }

  function next() {
    if (idx + 1 >= questions.length) {
      onFinished?.(score)
    } else {
      setIdx(i => i + 1)
      setSelected(null)
      setRevealed(false)
    }
  }

  const progress = useMemo(() => `${idx + 1} / ${questions.length}`, [idx, questions.length])

  return (
    <div className="card">
      <div className="row" style={{justifyContent:'space-between'}}>
        <h2>Question {progress}</h2>
        <div className="badge">Score: {score}</div>
      </div>
      <p style={{fontSize:18, lineHeight:1.5}}>{q.question}</p>
      <div style={{display:'grid', gap:12, marginTop:12}}>
        {q.options.map((opt, i) => {
          const isCorrect = opt === q.answer
          const className = revealed ? (isCorrect ? 'option correct' : (opt === selected ? 'option wrong' : 'option')) : 'option'
          return (
            <div key={i} className={className} onClick={() => choose(opt)}>
              {opt}
            </div>
          )
        })}
      </div>
      {revealed && q.explanation && (
        <p style={{marginTop:12, color:'#9fb3d1'}}>Explanation: {q.explanation}</p>
      )}
      <div className="row" style={{marginTop:16}}>
        <button onClick={next}>{idx + 1 >= questions.length ? 'Finish' : 'Next'}</button>
      </div>
    </div>
  )
}

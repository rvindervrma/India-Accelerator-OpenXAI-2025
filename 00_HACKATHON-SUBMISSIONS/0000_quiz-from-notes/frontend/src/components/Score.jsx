export default function Score({ score, total, onRestart }) {
  const pct = Math.round((score / total) * 100)
  return (
    <div className="card text-center">
      <h2>Your Score</h2>
      <p style={{fontSize:42, margin:'8px 0'}}>{score} / {total}</p>
      <p className="text-muted">Accuracy: {pct}%</p>
      <button onClick={onRestart} style={{marginTop:14}}>Restart</button>
    </div>
  )
}

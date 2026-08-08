import React, { useState, useEffect } from 'react'

export default function App(){
  const [results, setResults] = useState(null)
  const [features, setFeatures] = useState([])
  const [values, setValues] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(()=>{
    async function load(){
      try{
        const r = await fetch('/features')
        if(!r.ok) throw new Error('Failed to load features')
        const j = await r.json()
        const feats = j.features || []
        setFeatures(feats)
        // initialize values with placeholders
        const init = {}
        feats.forEach(f => init[f.name] = f.placeholder ?? 0)
        setValues(init)
      }catch(e){
        setError(e.message)
      }finally{ setLoading(false) }
    }
    load()
  }, [])

  function handleChange(e, name){
    const v = e.target.value
    setValues(prev => ({...prev, [name]: v === '' ? '' : Number(v)}))
  }

  async function submit(){
    setError(null)
    // basic validation: required and numeric
    for(const f of features){
      const v = values[f.name]
      if(v === undefined || v === ''){ setError(`Missing value for ${f.name}`); return }
      if(isNaN(Number(v))){ setError(`Invalid number for ${f.name}`); return }
    }
    const payload = { rows: [values] }
    try{
      const r = await fetch('/score', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) })
      const j = await r.json()
      if(r.ok) setResults(j.results)
      else setError(JSON.stringify(j))
    }catch(e){ setError(e.message) }
  }

  if(loading) return <div className="container py-4">Loading form...</div>
  if(error && features.length===0) return <div className="container py-4 text-danger">{error}</div>

  return (
    <div className="container py-4">
      <h3>Loan Default Scoring (Dynamic Form)</h3>
      <div className="row">
        <div className="col-md-6">
          <div className="card p-3 mb-3">
            <h5>Inputs</h5>
            {features.map(f => (
              <div className="mb-2" key={f.name}>
                <label className="form-label">{f.name}</label>
                <input className="form-control" type="number" step="any" value={values[f.name] ?? ''} onChange={(e)=>handleChange(e,f.name)} />
              </div>
            ))}
            <div className="d-flex gap-2">
              <button className="btn btn-primary" onClick={submit}>Score</button>
              <button className="btn btn-secondary" onClick={()=>{ setResults(null); setValues(v=>{ const nv = {}; features.forEach(f=>nv[f.name]=f.placeholder??0); return nv }) }}>Reset</button>
            </div>
            {error && <div className="mt-2 text-danger">{error}</div>}
          </div>
        </div>
        <div className="col-md-6">
          <h5>Results</h5>
          {results ? (
            <table className="table table-sm"><thead><tr><th>#</th><th>prob_default</th><th>pred_default</th></tr></thead><tbody>
              {results.map(r=> <tr key={r.index}><td>{r.index}</td><td>{r.prob_default.toFixed(4)}</td><td>{r.pred_default}</td></tr>)}
            </tbody></table>
          ) : <div className="text-muted">No results yet</div>}
        </div>
      </div>
    </div>
  )
}

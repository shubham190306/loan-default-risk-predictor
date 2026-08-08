from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any
from pydantic import BaseModel
import traceback

from models.scoring import ModelWrapper

app = FastAPI(title='Loan Default Scoring API')

# Serve static frontend
app.mount('/static', StaticFiles(directory='app/static'), name='static')


class RowsPayload(BaseModel):
    rows: List[Dict[str, Any]]


@app.on_event('startup')
def load_model():
    global wrapper
    try:
        wrapper = ModelWrapper()
    except Exception as e:
        # keep wrapper as None; endpoints will return 503
        wrapper = None
        app.state.load_error = str(e)


@app.get('/health')
def health():
    if wrapper is None:
        return {'status': 'error', 'error': getattr(app.state, 'load_error', 'model not loaded')}
    return {'status': 'ok'}


@app.post('/score')
def score(payload: RowsPayload):
    if wrapper is None:
        raise HTTPException(status_code=503, detail='Model not loaded')
    try:
        import pandas as pd
        df = pd.DataFrame(payload.rows)
        scored = wrapper.predict_proba(df)
        preds = wrapper.predict(df)
        out = []
        for idx, row in df.iterrows():
            out.append({
                'index': int(idx),
                'prob_default': float(scored.iloc[idx]),
                'pred_default': int(preds.iloc[idx])
            })
        return {'n': len(out), 'results': out}
    except Exception as e:
        traceback_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail={'error': str(e), 'trace': traceback_str})


@app.get('/metadata')
def metadata():
    if wrapper is None:
        raise HTTPException(status_code=503, detail='Model not loaded')
    return {'model_path': wrapper.model_path, 'threshold': wrapper.threshold}


@app.get('/', response_class=HTMLResponse)
def root():
    try:
        with open('app/static/index.html', 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except Exception:
        raise HTTPException(status_code=404, detail='Frontend not found')


@app.get('/features')
def features():
    # Return feature metadata for dynamic form generation
    try:
        # prefer features.json on disk
        import json
        if os.path.exists('models/features.json'):
            with open('models/features.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        # else try wrapper
        if wrapper is None:
            raise HTTPException(status_code=503, detail='Model not loaded')
        feats = getattr(wrapper, 'features', None)
        if feats is None:
            raise HTTPException(status_code=404, detail='Features not available')
        # normalize to feature metadata
        return {'features': [{'name': n, 'type': 'number', 'placeholder': 0} for n in feats]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=False)

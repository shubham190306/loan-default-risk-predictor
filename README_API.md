Loan Default Scoring API

Quickstart

1. Create and activate your Python environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run the API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. Example request (curl):

```bash
curl -X POST localhost:8000/score -H "Content-Type: application/json" -d \
  '{"rows": [{"int_rate": 0.12, "loan_amnt": 5000, "dti": 10}, {"int_rate": 0.2, "loan_amnt": 15000, "dti": 30}]}'
```

Notes
- Ensure `models/xgb_calibrated_sigmoid.pkl` and `models/xgb_final_metadata.json` exist in the `models/` folder before starting the server.
- The input rows must contain the same features (column names) used during training.
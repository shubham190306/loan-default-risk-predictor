# Loan Default Risk Predictor

This is a notebook-first machine-learning project for estimating the
probability that a LendingClub loan will be **Charged Off or Default**.

The project is intentionally kept small: the notebook contains the analysis,
feature engineering, model loading, scoring flow, and validation checks. It is
decision-support work, not an approval engine or an adverse-action notice. The
historical data and the exported model require independent validation before
any operational use.

## Start here

The complete workflow is in:

```text
notebooks/loan_default_modeling.ipynb
```

Run it from the repository root. The default mode validates the existing model
bundle and scores example applications without scanning the full CSV. Set
`LOAN_RUN_REBUILD=1` before executing the notebook only when you intentionally
want to retrain from the large accepted-loans file.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
jupyter lab
```

The notebook uses the following production artifacts:

- `models/xgb_calibrated_sigmoid.pkl` — calibrated XGBoost classifier
- `models/xgb_final_metadata.json` — release metadata and operating threshold
- `models/preprocessing.json` — raw input contract and frozen feature transform

The saved operating threshold is recorded in `models/xgb_final_metadata.json`.
The notebook checks that the raw application contract produces the expected
finite model features in the expected order.

## Data

- `accepted_2007_to_2018Q4.csv` contains application fields and loan outcomes
  used for supervised modeling.

The CSV files are large and should not be loaded into memory all at once. The
notebook uses header-only reads and small samples in review mode, then chunked
reads when rebuilding.

## Reproducibility notes

The retraining workflow uses 2015 for model fitting, 2016 for sigmoid
calibration, 2017 for threshold selection, and 2018 for final testing. It fits
learned preprocessing values on the training period only and records split
metrics, checksums, and the threshold objective in the model metadata. The
source provides terminal statuses rather than a fixed outcome horizon, so the
bundle still requires independent maturity, stability, and fairness review
before operational use.

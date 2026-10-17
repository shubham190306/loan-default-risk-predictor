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
`RUN_REBUILD = True` in the first code cell only when you intentionally want
to build a candidate model from the large accepted-loans file.

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

The saved operating threshold is `0.24644936516445318`. The notebook checks
that the raw application contract produces exactly 148 finite model features in
the expected order.

## Data

- `accepted_2007_to_2018Q4.csv` contains application fields and loan outcomes
  used for supervised modeling.

The CSV files are large and should not be loaded into memory all at once. The
notebook uses header-only reads and small samples in review mode, then chunked
reads when rebuilding.

## Reproducibility notes

The model bundle was trained on accepted loans issued from 2015 onward with a
terminal status. A future release should use a time-aware train/validation/test
split, fit preprocessing statistics on the training partition only, document
the threshold objective, and evaluate subgroup stability and fairness before
promotion.

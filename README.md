# PaySim Fraud Detection

Machine learning project for real-time payment fraud detection on the PaySim synthetic transaction dataset.

This repository was audited for data leakage. The current modeling notebook uses a T0-safe feature whitelist, chronological train/test split, profit-curve threshold optimization, and ROC/Lift monitoring.

## Current Results

These results come from `notebooks/03_modeling.ipynb` after removing leakage-prone raw balance columns and replacing random split with a chronological split.

| Metric | Value |
|---|---:|
| Test fraud base rate | 0.747% |
| LightGBM ROC-AUC | 0.9036 |
| LightGBM Average Precision | 0.3955 |
| Lift @ top 10% | 7.49x |
| Fraud capture @ top 10% | 74.87% |
| Lift @ top 20% | 4.25x |
| Fraud capture @ top 20% | 84.94% |
| Profit-curve threshold | 0.99290966 |
| Model alert rate | 0.2242% |
| Saving vs rule baseline | 1.52B VND, 22.73% |

The previous claim `AP=0.856` and `77% cost savings` is deprecated. It was based on a pipeline that mixed target-aware sampling/evaluation bias and leakage-prone balance fields.

## Modeling Pipeline

1. Load PaySim raw data.
2. Filter scoring scope using T0-available fields: `TRANSFER`/`CASH_OUT` and customer destinations.
3. Split by transaction time (`step`) so the test set is strictly later than train.
4. Balance only the training set.
5. Build model features with a whitelist from `src.features.MODEL_FEATURE_COLUMNS`.
6. Train RF, XGBoost, and LightGBM.
7. Evaluate on production-like chronological test data.
8. Select deployment threshold with a profit curve.
9. Monitor model ranking quality with ROC and Lift curves.

## T0-Safe Features

Current model features:

- `amount`
- `is_high_risk_type`
- `log_amount`
- `hour`
- `is_night`
- `is_dest_zero_balance`
- `high_risk_combo`

Raw balance fields are intentionally blocked from the model frame:

- `oldbalanceOrg`
- `newbalanceOrig`
- `oldbalanceDest`
- `newbalanceDest`
- `isFlaggedFraud`

`is_dest_zero_balance` is retained as a business hypothesis, but in production it must be backed by a pre-authorization balance snapshot. If that snapshot is not available at decision time, this feature must be replaced with safer account-history features such as prior transaction count, account age, or first-seen indicators.

## Business Evaluation

The current cost matrix is cost-only:

- False negative: missed fraud amount is lost.
- False positive: operational/customer-friction cost is paid.
- True positive is not counted again as positive benefit, which avoids TP/FN double counting.

Current optimized threshold result:

| Item | Value |
|---|---:|
| Approve-all loss | 6.74B VND |
| Rule-based loss | 6.67B VND |
| ML optimized loss | 5.16B VND |
| Saving vs rule | 1.52B VND |
| Saving vs rule rate | 22.73% |
| Profit vs approve-all | 1.59B VND |

## Project Structure

```text
fraud-detection-paysim/
├── data/raw/Synthetic_Financial_datasets_log.csv
├── models/LightGBM_model.pkl
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_eng.ipynb
│   └── 03_modeling.ipynb
├── src/
│   ├── data_loader.py
│   ├── features.py
│   └── model_eval.py
└── README.md
```

## Key Files

- `src/features.py`: T0-safe feature whitelist and leakage guards.
- `src/data_loader.py`: chronological split and train-only class balancing.
- `src/model_eval.py`: cost matrix, profit curve, ROC curve, and lift curve helpers.
- `notebooks/03_modeling.ipynb`: current end-to-end training and evaluation notebook.

## Run

```bash
python -m compileall src
python -m jupyter nbconvert --to notebook --execute notebooks/03_modeling.ipynb --inplace --ExecutePreprocessor.timeout=900
```

## Notes

PaySim is synthetic data, so this project is safe for public portfolio use. The production interpretation still requires validating field availability at transaction authorization time, especially for any balance-derived feature.

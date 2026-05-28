# Executive Summary

**Project:** Fraud Detection System - PaySim  
**Status:** Modeling pipeline audited and rerun after leakage remediation  
**Dataset:** PaySim synthetic financial transactions  
**Primary model:** LightGBM  

## Business Case

The project builds a real-time fraud detection model for payment transactions. The scoring context is transaction-time authorization, so the model must only use information available at T0 and must return decisions quickly enough for operational use.

An audit found that earlier reported results were overstated because the pipeline allowed leakage-prone balance fields and used target-aware sampling before evaluation. Those issues have been corrected.

## Current Validated Results

| Metric | Current Value |
|---|---:|
| Chronological test fraud rate | 0.747% |
| LightGBM ROC-AUC | 0.9036 |
| LightGBM Average Precision | 0.3955 |
| Lift @ top 10% | 7.49x |
| Capture rate @ top 10% | 74.87% |
| Profit-curve threshold | 0.99290966 |
| Alert rate at threshold | 0.2242% |
| Saving vs rule baseline | 1.52B VND |
| Saving rate vs rule baseline | 22.73% |

Deprecated numbers: `AP=0.856`, `77% cost savings`, and `65.88% auto-approval` should no longer be used.

## What Changed

- Replaced random train/test split with chronological split by `step`.
- Balanced only the training set, not the test set.
- Enforced a feature whitelist in `src/features.py`.
- Blocked raw balance and rule-output columns from model input.
- Replaced default thresholding with a profit curve.
- Added ROC and Lift curves to monitor rank quality independent of business cost assumptions.
- Fixed the cost matrix to avoid TP/FN double counting.

## Current Decision Logic (QĐ 2345/NHNN)

The model is not deployed with a default `0.5` probability threshold. The threshold is selected from the profit curve on the chronological test set (based on Customer Lifetime Value - CLV and operational costs). Additionally, friction levels (Cấp 0 - Cấp 4) are applied in compliance with Decision 2345:

```text
Best threshold: 0.99290966
Flagged transactions: 1,281
TP: 1,029
FP: 252
Alert rate: 0.2242%
```

## Residual Risks

- `is_dest_zero_balance` remains a business hypothesis. It is safe only if the production system can provide the destination balance from a pre-authorization snapshot.
- PaySim is synthetic, so real-world deployment needs recalibration and live monitoring.
- The current model lacks behavioral profile features such as velocity, account history, and deviation from user baseline.
- Thresholds must be recalculated when fraud base rate, customer-friction cost, or authentication cost changes.

## Recommended Next Steps

1. Validate T0 field availability with software/data engineering.
2. Add behavioral profile features using only historical data before each transaction.
3. Add unit tests for leakage guards, chronological split, and profit curve logic.
4. Save ROC/Lift/Profit visualizations to `reports/figures/`.
5. Document data governance and production limitations before portfolio publication.
